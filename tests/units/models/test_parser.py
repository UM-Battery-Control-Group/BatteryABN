import os
import pytest

from batteryabn.utils import Parser


BASE_DATA_PATH = BASE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
NEWARE_PATH = os.path.join(BASE_DATA_PATH, 'neware')
NEWARE_VDF_PATH = os.path.join(BASE_DATA_PATH, 'neware_vdf')

@pytest.mark.parser
def test_bad_file_path():
    parser = Parser()
    with pytest.raises(FileNotFoundError):
        parser.parse('bad_file_path')

@pytest.mark.parser
@pytest.mark.neware
def test_parser_neware():
    paths = [
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
    ]
    parser = Parser()

    for path in paths:
        parser.parse(path)
        assert parser.test_type == 'Neware'
        assert parser.raw_test_data.shape[0] > 0
        assert 'Voltage(V)'.lower() in parser.raw_test_data.columns.str.lower()
        assert 'Timestamp'.lower() in parser.raw_test_data.columns.str.lower()
        assert 'Date'.lower() in parser.raw_test_data.columns.str.lower()
        assert 'Total Time'.lower() in parser.raw_test_data.columns.str.lower()

@pytest.mark.parser
@pytest.mark.neware_vdf
def test_parser_neware_vdf():
    paths = [
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
    ]
    parser = Parser()

    for path in paths:
        parser.parse(path)
        assert parser.test_type == 'Neware_Vdf'
        assert parser.raw_test_data.shape[0] > 0
        assert 'LDC SENSOR'.lower() in parser.raw_test_data.columns.str.lower()
