from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository, FileSystemRepository
from batteryabn.services import CellService
from batteryabn.utils import Processor, Viewer
from batteryabn.app import create_app
from batteryabn.models import db

app = create_app()

with app.app_context():
    db.create_all()
    cell_repository = CellRepository() 
    test_record_repository = TestRecordRepository()
    project_repository = ProjectRepository()
    filesystem_repository = FileSystemRepository()
    cell_service = CellService(cell_repository, test_record_repository, project_repository, filesystem_repository)
    processor = Processor()
    viewer = Viewer()

    cell_names = [f"GMJULY2022_CELL{str(i).zfill(3)}" for i in [12, 98]]

    for cell_name in cell_names:
        cell_service.process_cell(cell_name, processor, viewer) 
        # df = cell_service.get_combined_cell_data(cell_name, processor)