import os
import pytest

from batteryabn import Constants
from batteryabn.utils import Parser, Formatter

BASE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
NEWARE_PATH = os.path.join(BASE_DATA_PATH, 'neware')
NEWARE_VDF_PATH = os.path.join(BASE_DATA_PATH, 'neware_vdf')

NEWARE_DATA_COLUMNS = []
NEWARE_VDF_DATA_COLUMNS = []


@pytest.mark.formatter
@pytest.mark.neware
def test_parser_neware():
    paths = [
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
    ]
    parser = Parser()
    formatter = Formatter()

    for path in paths:
        parser.parse(path)
        formatter.format_test_data(parser.raw_test_data, parser.test_type)
        formatter.format_metadata(parser.raw_metadata)

        assert 'cell temperature (c)' in formatter.test_data.columns
        for key in Constants.NEWARE_NAME_KEYS:
            assert key in formatter.metadata
        assert formatter.cell_name == 'GMJuly2022_CELL002'

@pytest.mark.formatter
@pytest.mark.neware_vdf
def test_parser_neware_vdf():
    paths = [
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
    ]
    parser = Parser()
    formatter = Formatter()

    for path in paths:
        parser.parse(path)
        formatter.format_test_data(parser.raw_test_data, parser.test_type)
        formatter.format_metadata(parser.raw_metadata)
        
        assert 'time' in formatter.test_data.columns
        assert 'timestamp' in formatter.test_data.columns
        assert 'voltage(v)' in formatter.test_data.columns
        assert 'current(a)' in formatter.test_data.columns
        assert 'ambient temperature (c)' in formatter.test_data.columns
        for key in Constants.NEWARE_VDF_NAME_KEYS:
            assert key in formatter.metadata
        assert formatter.cell_name == 'GMJuly2022_CELL002'