import os
from flask import Blueprint, jsonify
from flask_injector import inject
from batteryabn.services import CellService
from batteryabn.extensions import rq
from batteryabn.tasks import process_cell_task, update_trs_task

tasks_bp = Blueprint('tasks', __name__)

@inject 
@tasks_bp.route('/trs/update/<cell_name>', methods=['POST'])
def update_trs(cell_name: str, cell_service: CellService):
    """
    Update test records for a cell by its name.
    """
    cell = cell_service.find_cell_by_name(cell_name)
    if not cell:
        return jsonify({"error": "Cell not found"}), 404
    project_name = cell.project_name

    # TODO: Path should be hidden in the configuration file. Path should not be passed as an argument.
    data_directory = f'/home/me-bcl/Lab_share_Volt/PROJ_{project_name}/Cycler_Data_By_Cell/{cell_name}'
    # Check if the path is correct
    if not os.path.exists(data_directory):
        return jsonify({"error": "Data directory not found"}), 404
    
    update_trs_task.queue(data_directory, cell_name, False)
    return jsonify({"message": "Test records update task enqueued."})

@inject 
@tasks_bp.route('/trs/reset/<cell_name>', methods=['POST'])
def reset_trs(cell_name: str, cell_service: CellService):
    """
    Reset test records for a cell by its name.
    """
    cell = cell_service.find_cell_by_name(cell_name)
    if not cell:
        return jsonify({"error": "Cell not found"}), 404
    project_name = cell.project_name
    # TODO: Path should be hidden in the configuration file. Path should not be passed as an argument.
    data_directory = f'/home/me-bcl/Lab_share_Volt/PROJ_{project_name}/Cycler_Data_By_Cell/{cell_name}'
    # Check if the path is correct
    if not os.path.exists(data_directory):
        return jsonify({"error": "Data directory not found"}), 404
    
    update_trs_task.queue(data_directory, cell_name, True)
    return jsonify({"message": "Test records update task enqueued."})

@inject
@tasks_bp.route('/cell/create/<cell_name>', methods=['POST'])
def create_cell(cell_name: str):
    """
    Create a cell by its name.
    """
    project_name = cell_name.split('_')[0]
    # TODO: Path should be hidden in the configuration file. Path should not be passed as an argument.
    data_directory = f'/home/me-bcl/Lab_share_Volt/PROJ_{project_name}/Cycler_Data_By_Cell/{cell_name}'
    # Check if the path is correct
    if not os.path.exists(data_directory):
        return jsonify({"error": "Cell does not have data here"}), 404

    update_trs_task.queue(data_directory, cell_name, True)
    return jsonify({"message": "Test records update task enqueued."})
    

@inject
@tasks_bp.route('/cell/process/<cell_name>', methods=['POST'])
def process_cell(cell_name: str, cell_service: CellService):
    """
    Process a cell by its name.
    """
    cell = cell_service.find_cell_by_name(cell_name)
    if not cell:
        return jsonify({"error": "Cell not found"}), 404
    process_cell_task.queue(cell_name)
    return jsonify({"message": "Cell processing task enqueued."})


@inject
@tasks_bp.route('/status', methods=['GET'])
def get_all_tasks_status():
    """
    Get the status of all tasks.
    """
    queue = rq.get_queue()
    started_registry = queue.started_job_registry
    finished_registry = queue.finished_job_registry
    failed_registry = queue.failed_job_registry
    def fetch_job_details(job_id):
        job = queue.fetch_job(job_id)
        if job is None:
            return {"id": job_id, "status": "unknown"}
        return {
            "id": job.id,
            "status": job.get_status(),
            "enqueued_at": job.enqueued_at.strftime('%Y-%m-%d %H:%M:%S') if job.enqueued_at else None,
            "started_at": job.started_at.strftime('%Y-%m-%d %H:%M:%S') if job.started_at else None,
            "ended_at": job.ended_at.strftime('%Y-%m-%d %H:%M:%S') if job.ended_at else None,
        }
    result = {
        "queued": [
            {"id": job.id, "status": job.get_status(), "enqueued_at": job.enqueued_at.strftime('%Y-%m-%d %H:%M:%S')}
            for job in queue.jobs
        ],
        "started": [fetch_job_details(job_id) for job_id in started_registry.get_job_ids()],
        "finished": [fetch_job_details(job_id) for job_id in finished_registry.get_job_ids()],
        "failed": [fetch_job_details(job_id) for job_id in failed_registry.get_job_ids()],
    }

    return jsonify(result), 200
