import pytest
from unittest.mock import MagicMock
from batteryabn.models import TestRecord
from batteryabn.repositories.testrecord_repository import TestRecordRepository

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def test_record_repository(mock_session):
    return TestRecordRepository(mock_session)

@pytest.mark.testrecord
def test_save(mock_session, test_record_repository):
    test_record = TestRecord(test_name="Test 1", cell_name="Cell 1")
    test_record_repository.save(test_record)

    mock_session.add.assert_called_once_with(test_record)
    mock_session.commit.assert_called_once()

@pytest.mark.testrecord
def test_find_by_name(mock_session, test_record_repository):
    mock_return_value = TestRecord(test_name="Test 1", cell_name="Cell 1")
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_return_value
    
    result = test_record_repository.find_by_name("Test 1")

    assert result == mock_return_value
    mock_session.query(TestRecord).filter_by.assert_called_with(test_name="Test 1")

@pytest.mark.testrecord
def test_find_by_cell_name(mock_session, test_record_repository):
    mock_return_value = [TestRecord(test_name="Test 1", cell_name="Cell 1"), TestRecord(test_name="Test 2", cell_name="Cell 1")]
    mock_session.query.return_value.filter_by.return_value.all.return_value = mock_return_value

    result = test_record_repository.find_by_cell_name("Cell 1")

    assert result == mock_return_value
    mock_session.query(TestRecord).filter_by.assert_called_with(cell_name="Cell 1")
