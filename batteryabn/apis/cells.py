from flask import Blueprint, jsonify
from flask_injector import inject
from batteryabn.services import CellService

cells_bp = Blueprint('cells', __name__)

@inject
@cells_bp.route('/<project_name>', methods=['GET'])
def get_cells_by_project(project_name: str, cell_service: CellService):
    """
    Get cells by project name or cell name.
    """    
    cells = cell_service.find_cells_by_project_name(project_name)
    if not cells:
        return jsonify({"error": "The project does not exist or has no cells."}), 404
    return jsonify([cell.to_dict() for cell in cells])


@inject
@cells_bp.route('/<cell_name>', methods=['GET'])
def get_cell_by_name(cell_name: str, cell_service: CellService):
    """
    Get a specific cell by its name.
    """
    cell = cell_service.find_cell_by_name(cell_name)
    if not cell:
        return jsonify({"error": "Cell not found"}), 404
    return jsonify(cell.to_dict())
