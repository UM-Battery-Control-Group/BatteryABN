from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository
from batteryabn.services import CellService
from batteryabn.utils import Processor, Viewer
from batteryabn.models import Session

session = Session()
processor = Processor()
viewer = Viewer()
cell_repository = CellRepository(session)
test_record_repository = TestRecordRepository(session)
project_repository = ProjectRepository(session)
cell_service = CellService(cell_repository, test_record_repository, project_repository)

cell_name = 'GMJuly2022_CELL002'

cell = cell_service.create_cell(cell_name)

cell_service.process_cell(cell_name, processor, viewer) 

