import os
from flask import Blueprint, jsonify
from flask_injector import inject
from rq.job import Job
from rq.registry import FinishedJobRegistry, FailedJobRegistry, StartedJobRegistry
from batteryabn.services import TestRecordService, CellService, ProjectService
from batteryabn.utils import Parser, Formatter, Processor, Viewer
from batteryabn.extensions import task_queue, redis_conn

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
    
    task_queue.enqueue(update_trs_task, data_directory, cell_name, False)
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
    
    task_queue.enqueue(update_trs_task, data_directory, cell_name, True)
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
    
    task_queue.enqueue(update_trs_task, data_directory, cell_name, True)
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
    task_queue.enqueue(process_cell_task, cell_name)
    return jsonify({"message": "Cell processing task enqueued."})


@inject
@tasks_bp.route('/status', methods=['GET'])
def get_all_tasks_status():
    """
    Get the status of all tasks.
    """
    queued_jobs = task_queue.jobs 

    started_registry = StartedJobRegistry(queue=task_queue)
    finished_registry = FinishedJobRegistry(queue=task_queue)
    failed_registry = FailedJobRegistry(queue=task_queue)
    
    started_jobs = started_registry.get_job_ids()
    finished_jobs = finished_registry.get_job_ids()
    failed_jobs = failed_registry.get_job_ids()

    def fetch_job_details(job_id):
        job = Job.fetch(job_id, connection=redis_conn)
        return {
            "id": job.id,
            "status": job.get_status(),
            "enqueued_at": job.enqueued_at.strftime('%Y-%m-%d %H:%M:%S') if job.enqueued_at else None
        }

    result = {
        "queued": [{"id": job.id, "status": job.get_status(), "enqueued_at": job.enqueued_at.strftime('%Y-%m-%d %H:%M:%S')} for job in queued_jobs],
        "started": [fetch_job_details(job_id) for job_id in started_jobs],
        "finished": [fetch_job_details(job_id) for job_id in finished_jobs],
        "failed": [fetch_job_details(job_id) for job_id in failed_jobs],
    }

    return jsonify(result), 200


@inject
def process_cell_task(cell_name: str, cell_service: CellService, processor: Processor, viewer: Viewer):
    """
    Function called by the task queue to process a cell by its name.
    """
    cell_service.process_cell(cell_name, processor, viewer)
    return

@inject
def update_trs_task(data_directory: str, cell_name: str, reset: bool, test_record_service: TestRecordService, parser: Parser, formatter: Formatter):
    """
    Function called by the task queue to update test records for a cell by its name.
    """
    test_record_service.create_and_save_trs(data_directory, cell_name, parser, formatter, reset)
    return
