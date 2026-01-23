from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository, FileSystemRepository
from batteryabn.services import CellService, TestRecordService
from batteryabn.utils import Processor, Viewer
from batteryabn.app import create_app
from batteryabn.extensions import db
import matplotlib.pyplot as plt

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        cell_repository = CellRepository()
        test_record_repository = TestRecordRepository()
        project_repository = ProjectRepository()
        filesystem_repository = FileSystemRepository()
        cell_service = CellService(cell_repository, test_record_repository, project_repository, filesystem_repository)
        test_record_service = TestRecordService(cell_repository, test_record_repository, project_repository)

        viewer=Viewer()
        # cell_name = 'SANDIATENERGY_CELL002'
        cell_name = 'UMBL2022FEB_CELL152001'
        cell_name ='LGM50LT_CELL004'
        # cell_name = 'GMJULY2022_CELL042'
        # Load the proecssed data for the cell
        cell = cell_service.find_cell_by_name(cell_name)
        # cells = cell_service.find_cells_by_keyword('GMJULY2022')
        print(cell.cell_name)
        print(cell.project_name)
        print(f"Start loading data for {cell_name}")
        cell_data, cell_cycle_metrics, cell_data_vdf, cell_data_rpt = cell_service.get_processed_data(cell_name)
        print(cell_data.tail())
        print(cell_cycle_metrics.tail())
        # print(cell_data_vdf.columns)

        img_cell, img_ccm, img_ccm_aht, img_cell_html, img_ccm_html, img_ccm_aht_html = viewer.plot(cell_data, cell_cycle_metrics, cell_data_vdf, cell_name)
        
        plt.show()
        # Search for trs for cell
        # cycler_trs, vdf_trs = cell_service.get_cycler_vdf_trs(cell)
        # for tr in cycler_trs:
        #     print(tr)
        # for tr in vdf_trs:
        #     print(tr)
        
        # Load individual tr by name
        # # tr = test_record_service.find_test_record_by_name('GMFEB23S_CELL019_Test7-soc50100-Cby3-n100_1_P25C_15P0PSI_20240205_R0', 'Arbin')
        # tr = test_record_service.find_test_record_by_name('UMBL2022FEB_CELL152041_TestCYC_2C2CR1_1_P45C_5P0PSI_20231114_R0_CH108','Vdf')
        # print(tr.test_name)
        # print(tr.cell_name)
        # tr_data = tr.get_test_data()
        # tr_meta_data = tr.get_test_metadata()
        # # print(tr_data['timestamp'].head())
        # print(tr_data.columns)
