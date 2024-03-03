import os
import pytest
import pandas as pd
import pickle
from unittest.mock import patch, MagicMock

from batteryabn.models import TestRecord, create_cell

test_data_df = pd.DataFrame({
    'time': [1, 2, 3, 4, 5],
    'voltage': [3.0, 3.1, 3.2, 3.3, 3.4],
    'current': [0.1, 0.2, 0.3, 0.4, 0.5]
})

@pytest.mark.testrecord
def test_load_from_file():
    path = "dummy_path"
    test_record = TestRecord()
    with patch('batteryabn.utils.parser.Parser') as MockParser, \
         patch('batteryabn.utils.formatter.Formatter') as MockFormatter:
        mock_parser = MockParser.return_value
        mock_formatter = MockFormatter.return_value
        
        mock_parser.parse.return_value = None
        mock_parser.test_name = "TestName"
        mock_parser.test_type = "TestType"
        mock_parser.raw_test_data = test_data_df
        mock_parser.raw_metadata = {"Project Name": "Project1", "Cell ID": "CellName"}
        mock_formatter.cell_name = "Project1_CellName"
        mock_formatter.test_data = test_data_df
        mock_formatter.metadata = {"metadata": "dummy"}  

        test_record.load_from_file(path, mock_parser, mock_formatter) 

        assert test_record.test_name == "TestName"
        assert test_record.test_type == "TestType"
        assert test_record.cell_name == "Project1_CellName"
        loaded_test_data = pickle.loads(test_record.test_data)
        pd.testing.assert_frame_equal(loaded_test_data, test_data_df)


@pytest.mark.testrecord
def test_save_to_db_cell_not_found():
    mock_session = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    test_record = TestRecord()
    test_record.cell_name = "GMJuly2022_CELL002"
    test_record.test_name = "TestName"

    # Mock the create_cell function to return a mock Cell instance
    with patch('batteryabn.models.testrecord.create_cell') as mock_create_cell:
        mock_cell = MagicMock()
        mock_create_cell.return_value = mock_cell  # Mock the create_cell function to return a mock Cell instance
        
        test_record.save_to_db(mock_session)

        mock_create_cell.assert_called_once_with("GMJuly2022_CELL002")
        mock_session.add.assert_any_call(mock_cell)
        mock_session.add.assert_any_call(test_record)
        mock_session.commit.assert_called_once()
        assert test_record.cell == mock_cell, "TestRecord.cell should be set to the mock Cell instance"

@pytest.mark.testrecord
def test_save_to_db_cell_found():
    mock_session = MagicMock()
    # Create a mock Cell instance
    mock_cell = MagicMock()
    # Mock the query to return the mock Cell instance
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_cell

    # Create a TestRecord instance
    test_record = TestRecord()
    test_record.cell_name = "GMJuly2022_CELL002"
    test_record.test_name = "TestName"

    # Call the save_to_db method
    test_record.save_to_db(mock_session)

    # Verify that the mock Cell instance is associated with the TestRecord
    assert test_record.cell == mock_cell, "TestRecord.cell should be set to the found Cell instance"

    mock_session.add.assert_called_with(test_record)
    mock_session.commit.assert_called_once()
        