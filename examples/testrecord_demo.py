import os
from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository
from batteryabn.services import TestRecordService
from batteryabn.utils import Parser, Formatter
from batteryabn.models import Session

current_directory = os.path.dirname(__file__)

data_directory = os.path.join(current_directory, '..', 'tests', 'data')
neware_vdf_path = os.path.join(data_directory, 'neware_vdf')
neware_path = os.path.join(data_directory, 'neware')

paths = [
    os.path.join(neware_path, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
    os.path.join(neware_path, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
    os.path.join(neware_vdf_path, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
]

session = Session()
parser = Parser()
formatter = Formatter()
cell_repository = CellRepository(session)
test_record_repository = TestRecordRepository(session)
project_repository = ProjectRepository(session)
test_record_service = TestRecordService(cell_repository, test_record_repository, project_repository)

for path in paths:
    test_record_service.create_and_save_tr(path, parser, formatter)

# Check that the test records were added to the database
trs = test_record_service.find_test_records_by_cell_name('GMJuly2022_CELL002')
for tr in trs:
    print(f"Test Record: {tr.test_name}")
    print(tr.get_test_data().columns)
    print(tr.get_test_metadata())

tr = test_record_service.find_test_record_by_name('GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1')
print(f"Test Record: {tr.test_name}")

# Check that the cell was added to the database
cell = cell_repository.find_by_name('GMJuly2022_CELL002')
print(f"Cell: {cell.cell_name}")




