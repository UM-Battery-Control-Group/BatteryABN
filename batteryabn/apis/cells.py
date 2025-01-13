from flask import Blueprint, jsonify, send_file
from flask_injector import inject
from batteryabn.services import CellService

cells_bp = Blueprint('cells', __name__)

@inject
@cells_bp.route('/project/<project_name>', methods=['GET'])
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


@inject
@cells_bp.route('/<cell_name>/images/<int:number>', methods=['GET'])    
def get_cell_images(cell_name: str, number: int, cell_service: CellService):
    """
    Get images for a cell.
    """

    #TODO: Temp solution since images saved in local file system
    image_paths =  cell_service.get_cell_imgs_paths(cell_name)
    if not image_paths or number < 0 or number >= len(image_paths):
        return jsonify({"error": "Images not found"}), 404
    images = image_paths[number]
    return send_file(images, mimetype='image/png')

@inject
@cells_bp.route('/<cell_name>/htmls/<int:number>', methods=['GET'])    
def get_cell_htmls(cell_name: str, number: int, cell_service: CellService):
    """
    Get html files for a cell.
    """
    html_paths =  cell_service.get_cell_htmls_paths(cell_name)
    if not html_paths or number < 0 or number >= len(html_paths):
        return jsonify({"error": "Html files not found"}), 404
    html = html_paths[number]
    return send_file(html, mimetype='text/html')

@inject
@cells_bp.route('/search/<keyword>', methods=['GET'])
def search_cells(keyword: str, cell_service: CellService):
    """
    Search cells by keyword.
    """
    cells = cell_service.find_cells_by_keyword(keyword)
    if not cells:
        return jsonify({"error": "No cells found"}), 404
    return jsonify([cell.to_dict() for cell in cells])

@inject
@cells_bp.route('/<cell_name>/trs/latest', methods=['GET'])
def get_latest_tr(cell_name: str, cell_service: CellService):
    """
    Get the latest test record for a cell.
    """
    test_record = cell_service.get_latest_test_record(cell_name)
    if test_record is None:
        return jsonify({"error": "Test record not found"}), 404
    return jsonify(test_record.to_dict())

@inject
@cells_bp.route('/<cell_name>/info/latest', methods=['GET'])
def get_latest_info(cell_name: str, cell_service: CellService):
    """
    Get the latest info for a cell.
    """
    rpt_info = cell_service.get_latest_cell_info(cell_name)
    if rpt_info is None:
        return jsonify({"error": "Rpt info not found"}), 404
    return jsonify(rpt_info)


# TODO: Currently, the size of the binary data is too large to be returned as a response.
#       In the future, could use timescaledb to store the test data and return the data in chunks(separate by time).

# @inject
# @cells_bp.route('/<cell_name>/data/cell_data', methods=['GET'])
# def get_cell_data(cell_name: str, cell_service: CellService):
#     """
#     Get cell data by its name.
#     """
#     cell_data = cell_service.get_data(cell_name, 'cell_data')
#     if cell_data is None:
#         return jsonify({"error": "Cell data not found"}), 404
#     cell_data = cell_data.to_json(orient='records')
#     return jsonify(cell_data)

# @inject
# @cells_bp.route('/<cell_name>/data/cell_cycle_metrics', methods=['GET'])
# def get_cell_cycle_metrics(cell_name: str, cell_service: CellService):
#     """
#     Get cell cycle metrics by its name.
#     """
#     cell_cycle_metrics = cell_service.get_data(cell_name, 'cell_cycle_metrics')
#     if cell_cycle_metrics is None:
#         return jsonify({"error": "Cell cycle metrics not found"}), 404
#     cell_cycle_metrics = cell_cycle_metrics.to_json(orient='records')
#     return jsonify(cell_cycle_metrics)

# @inject
# @cells_bp.route('/<cell_name>/data/cell_data_vdf', methods=['GET'])
# def get_cell_data_vdf(cell_name: str, cell_service: CellService):
#     """
#     Get cell data VDF by its name.
#     """
#     cell_data_vdf = cell_service.get_data(cell_name, 'cell_data_vdf')
#     if cell_data_vdf is None:
#         return jsonify({"error": "Cell data VDF not found"}), 404
#     cell_data_vdf = cell_data_vdf.to_json(orient='records')
#     return jsonify(cell_data_vdf)
    