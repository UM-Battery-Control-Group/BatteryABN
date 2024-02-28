import os
from batteryabn.Testrecord import Parser, Formatter

current_directory = os.path.dirname(__file__)

data_directory = os.path.join(current_directory, '..', '..', 'tests', 'data')
neware_vdf_path = os.path.join(data_directory, 'neware_vdf')
neware_path = os.path.join(data_directory, 'neware')

neware_test_paths = [
    os.path.join(neware_path, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
]
neware_vdf_test_paths = [
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
]

parser = Parser()
formatter = Formatter()

for path in neware_test_paths:
    parser.parse(path)
    formatter.format_test_data(parser.raw_test_data, parser.test_type)
    formatter.format_metadata(parser.raw_metadata)

    print(formatter.test_data.head())

for path in neware_vdf_test_paths:
    parser.parse(path)
    formatter.format_test_data(parser.raw_cycler_data, parser.test_type, is_cycle=True)
    formatter.format_metadata(parser.raw_metadata)

    print(formatter.cycler_data.head())