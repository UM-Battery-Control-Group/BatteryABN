import os
import pytest

from batteryabn import Testrecord

BASE_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
NEWARE_PATH = os.path.join(BASE_DATA_PATH, 'neware')
NEWARE_VDF_PATH = os.path.join(BASE_DATA_PATH, 'neware_vdf')

@ pytest.mark.testrecord
@ pytest.mark.neware
def test_testrecord_neware():
    paths = [
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
    ]
    testrecord = Testrecord()

    for path in paths:
        testrecord.parse(path).format()
        assert testrecord.test_name == os.path.basename(path).split('.')[0]
        assert testrecord.test_type == 'Neware'
        assert 'cell temperature (c)' in testrecord.test_data.columns

@ pytest.mark.testrecord
@ pytest.mark.neware_vdf
def test_testrecord_neware_vdf():
    paths = [
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
    ]
    testrecord = Testrecord()

    for path in paths:
        testrecord.parse(path).format()
        assert testrecord.test_name == os.path.basename(path).split('.')[0]
        assert testrecord.test_type == 'Neware_Vdf'
        assert 'time' in testrecord.cycler_data.columns
        assert 'timestamp' in testrecord.cycler_data.columns
        assert 'voltage(v)' in testrecord.cycler_data.columns
        assert 'current(a)' in testrecord.cycler_data.columns
        assert 'ambient temperature (c)' in testrecord.cycler_data.columns