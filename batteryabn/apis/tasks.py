import os
from flask import Blueprint, jsonify
from flask_injector import inject
from batteryabn.services import CellService
from batteryabn.extensions import rq
from batteryabn.tasks import process_cell_task, update_trs_task, clear_failed, clear_finished, clear_all, get_tasks_status

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
    
    update_trs_task.queue(data_directory, cell_name, False, description=f"Update {cell_name}")
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
    
    update_trs_task.queue(data_directory, cell_name, True, description=f"Reset {cell_name}")
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

    update_trs_task.queue(data_directory, cell_name, True, description=f"Create {cell_name}")
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
    process_cell_task.queue(cell_name, description=f"Process {cell_name}")
    return jsonify({"message": "Cell processing task enqueued."})

@inject
@tasks_bp.route('/status', methods=['GET'])
def get_all_tasks_status():
    """
    Get the status of all tasks.
    """
    result = get_tasks_status()
    return jsonify(result), 200


@tasks_bp.route('/clear', methods=['POST'])
def clear_all_tasks():
    """
    Clear all tasks.
    """
    clear_all()
    return jsonify({"message": "All tasks cleared."}), 200

@tasks_bp.route('/clear/finished', methods=['POST'])
def clear_finished_tasks():
    """
    Clear finished tasks.
    """
    result = clear_finished()
    return jsonify(result), 200


@tasks_bp.route('/clear/failed', methods=['POST'])
def clear_failed_tasks():
    """
    Clear failed tasks.
    """
    result = clear_failed()
    return jsonify(result), 200
