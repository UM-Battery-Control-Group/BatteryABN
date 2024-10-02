from flask import Blueprint, jsonify
from flask_injector import inject
from batteryabn.services import TestRecordService

trs_bp = Blueprint('tests', __name__)


@inject
@trs_bp.route('/<cell_name>', methods=['GET'])
def get_trs_by_cell_name(cell_name: str, test_record_service: TestRecordService):
    """
    Get test records by test name or cell name.
    """
    trs = test_record_service.find_test_records_by_cell_name(cell_name)
    if not trs:
        return jsonify({"error": "The cell does not exist or has no test records."}), 404
    return jsonify([test.to_dict() for test in trs])

@inject
@trs_bp.route('/<tr_name>', methods=['GET'])
def get_tr_by_name(test_name: str, test_record_service: TestRecordService):
    """
    Get a specific test record by its name.
    """
    test_record = test_record_service.find_test_record_by_name(test_name)
    if not test_record:
        return jsonify({"error": "Test record not found"}), 404
    return jsonify(test_record.to_dict())



