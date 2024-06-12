import matplotlib.pyplot as plt
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

cell_name = 'GMJULY2022_CELL002'

cell_service.process_cell(cell_name, processor, viewer) 

cell = cell_service.find_cell_by_name(cell_name)

fig_ccm = cell.load_image_ccm()
fig_cll = cell.load_image_cell()
fig_ccm_aht = cell.load_image_ccm_aht()

plt.show()

combined_data = cell_service.get_combined_cell_data(cell_name, processor)
print(combined_data.columns)
print(f'Length of combined data: {len(combined_data)}') 