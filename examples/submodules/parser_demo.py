import os
from batteryabn.utils import Parser
import matplotlib

current_directory = os.path.dirname(__file__)

data_directory = os.path.join(current_directory, '..', '..', 'tests', 'data')
neware_vdf_path = os.path.join(data_directory, 'neware_vdf')
neware_path = os.path.join(data_directory, 'neware')
biologic_path = os.path.join(data_directory, 'biologic')

paths = [
    # os.path.join(neware_path, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
    # os.path.join(neware_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
    # os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
    # os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
    os.path.join(biologic_path, 'GMJuly2022_CELL089_EIS_2_P25C_5P0PSI_20230118_R0_CH005_02_BCD_CA5.mpr'),
    os.path.join(biologic_path, 'GMJuly2022_CELL089_EIS_2_P25C_5P0PSI_20230118_R1_CH005_01_MB_CA5.mpr'),
    os.path.join(biologic_path, 'GMJuly2022_CELL090_EIS_3db_P25C_15P0PSI_20231013_R0_CA7.mpr'),

]
parser = Parser()

for path in paths:
    parser.parse(path)
    print(parser.raw_test_data.columns)
    print(parser.raw_metadata)
    print(parser.test_type)

    print(parser.raw_test_data['Q charge/discharge/mA.h'])

