import os
import pytest
import pandas as pd
import pickle
from unittest.mock import patch, MagicMock

from batteryabn.models import TestRecord

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

        