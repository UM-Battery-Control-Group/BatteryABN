import pytest
from unittest.mock import MagicMock, patch
from batteryabn.models import TestRecord, Cell
from batteryabn.repositories import CellRepository, TestRecordRepository
from batteryabn.services.testrecord_service import TestRecordService
from batteryabn.utils import Parser, Formatter

# Mocking the dependencies of the TestRecordService
@pytest.fixture
def cell_repository_mock():
    return MagicMock(spec=CellRepository)

@pytest.fixture
def test_record_repository_mock():
    return MagicMock(spec=TestRecordRepository)

@pytest.fixture
def test_record_service(cell_repository_mock, test_record_repository_mock):
    return TestRecordService(cell_repository=cell_repository_mock, test_record_repository=test_record_repository_mock)

@pytest.fixture
def parser_mock():
    parser = MagicMock(spec=Parser)
    parser.test_name = "TestName"
    parser.test_type = "TestType"
    return parser

@pytest.fixture
def formatter_mock():
    formatter = MagicMock(spec=Formatter)
    formatter.cell_name = "TestCell"
    return formatter

@pytest.fixture
def cell_mock():
    cell = MagicMock(spec=Cell)
    cell.cell_name = "TestCell"
    # Mock the _sa_instance_state attribute to avoid the error: AttributeError: 'Mock' object has no attribute '_sa_instance_state'
    cell._sa_instance_state = MagicMock()
    return cell

@pytest.mark.testrecord
def test_create_and_save_tr_with_no_existing_cell(test_record_service, parser_mock, formatter_mock):
    path = "dummy_path"
    cell_name = "TestCell"
    test_record_service.cell_repository.find_by_name.return_value = None  # Mock return None for no existing cell
    test_record_service.test_record_repository.find_by_name.return_value = None # Mock return None for no existing test record

    with patch('batteryabn.models.TestRecord.load_from_file', autospec=True) as load_mock:
        test_record_service.create_and_save_tr(path, parser_mock, formatter_mock)

        load_mock.assert_called_once()
        test_record_service.cell_repository.create_cell.assert_called_once_with(cell_name)
        test_record_service.test_record_repository.save.assert_called()

@pytest.mark.testrecord
def test_create_and_save_tr_with_existing_cell(test_record_service, parser_mock, formatter_mock, cell_mock):
    path = "dummy_path"
    cell_name = "TestCell"

    test_record_service.cell_repository.find_by_name.return_value = cell_mock  # Mock return existing cell
    test_record_service.test_record_repository.find_by_name.return_value = None # Mock return None for no existing test record

    with patch('batteryabn.models.TestRecord.load_from_file', autospec=True) as load_mock:
        test_record_service.create_and_save_tr(path, parser_mock, formatter_mock)

        load_mock.assert_called_once()
        test_record_service.cell_repository.create_cell.assert_not_called()
        test_record_service.test_record_repository.save.assert_called()

@pytest.mark.testrecord
def test_find_test_record_by_name(test_record_service, test_record_repository_mock):
    test_name = "TestRecord1"
    mock_test_record = TestRecord(test_name=test_name)
    test_record_repository_mock.find_by_name.return_value = mock_test_record

    result = test_record_service.find_test_record_by_name(test_name)

    test_record_repository_mock.find_by_name.assert_called_once_with(test_name)
    assert result == mock_test_record

@pytest.mark.testrecord
def test_find_test_records_by_cell_name(test_record_service, test_record_repository_mock):
    cell_name = "TestCell"
    mock_test_records = [TestRecord(test_name="TestRecord1"), TestRecord(test_name="TestRecord2")]
    test_record_repository_mock.find_by_cell_name.return_value = mock_test_records

    result = test_record_service.find_test_records_by_cell_name(cell_name)

    test_record_repository_mock.find_by_cell_name.assert_called_once_with(cell_name)
    assert result == mock_test_records
