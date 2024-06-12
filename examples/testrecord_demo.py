import os
from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository
from batteryabn.services import TestRecordService
from batteryabn.utils import Parser, Formatter
from batteryabn.models import Session

current_directory = os.path.dirname(__file__)

data_directory = os.path.join(current_directory, '..', 'tests', 'data')
neware_vdf_path = os.path.join(data_directory, 'neware_vdf')
neware_path = os.path.join(data_directory, 'neware')
biologic_path = os.path.join(data_directory, 'biologic')

calibration_parameters_path = os.path.join(data_directory, 'sanity_check.csv')

paths = [
    os.path.join(neware_path, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041_20221011212336_37_2_1_2818580162.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL002_RPT_1_P25C_5P0PSI_20221108_R0_CH041_20221108185356_37_2_1_2818580172.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL002_RPT_3_P25C_5P0PSI_20230110_R0_CH041_20230110152642_37_2_1_2818580186.xlsx'),
    # os.path.join(neware_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221021_R0_CH041_20221021214726_37_2_1_2818580168_1.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221021_R0_CH041_20221021214726_37_2_1_2818580168.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL004_8c_1_P25C_25P0PSI_20220930_R0_CH032_20220930225635_36_4_8_2818579450.xlsx'),

    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_BOL_1_P0C_5P0PSI_20220907_R0_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_3_P25C_5P0PSI_20230110_R0_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221018_R0_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221021_R0_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL004_Diag_P25C_25P0PSI_20220902_R0_CH032.csv'),
    os.path.join(biologic_path, 'GMJuly2022_CELL090_EIS_3db_P25C_15P0PSI_20231013_R0_CA7.mpr'),
    os.path.join(biologic_path, 'GMJuly2022_CELL089_EIS_2_P25C_5P0PSI_20230118_R0_CH005_01_MB_CA5.mpr'),
    os.path.join(biologic_path, 'GMJuly2022_CELL089_EIS_2_P25C_5P0PSI_20230118_R0_CH005_02_BCD_CA5.mpr'),
    os.path.join(biologic_path, 'GMJuly2022_CELL089_EIS_2_P25C_5P0PSI_20230118_R1_CH005_01_MB_CA5.mpr'),
    os.path.join(biologic_path, 'GMJuly2022_CELL089_EIS_2_P25C_5P0PSI_20230118_R1_CH005_02_BCD_CA5.mpr'),

]

session = Session()
parser = Parser()
formatter = Formatter()
cell_repository = CellRepository(session)
test_record_repository = TestRecordRepository(session)
project_repository = ProjectRepository(session)
test_record_service = TestRecordService(cell_repository, test_record_repository, project_repository)

parser.parse_calibration_parameters(calibration_parameters_path)
formatter.format_calibration_parameters(parser.calibration_parameters)
# for path in paths:
#     test_record_service.create_and_save_tr(path, parser, formatter, reset=True)
test_record_service.create_and_save_trs(data_directory, key_word='GMJuly2022_CELL089', parser=parser, formatter=formatter, reset=True)

# Check that the test records were added to the database
# trs = test_record_service.find_test_records_by_cell_name('GMJuly2022_CELL002')
# for tr in trs:
#     print(f"Test Record: {tr.test_name}")
#     print(tr.get_test_data().columns)
#     print(tr.get_test_metadata())

# tr = test_record_service.find_test_record_by_name('GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1')
# print(f"Test Record: {tr.test_name}")

# Check that the cell was added to the database
cell = cell_repository.find_by_name('GMJuly2022_CELL089')
print(f"Cell: {cell.cell_name}")




