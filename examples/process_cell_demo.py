import multiprocessing
from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository, FileSystemRepository
from batteryabn.services import CellService
from batteryabn.utils import Processor, Viewer
from batteryabn.app import create_app
from batteryabn.extensions import db
from tqdm import tqdm


def process_cell_in_parallel(cell_name):
    try:
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
            cell_service.process_cell(cell_name, processor, viewer)
    except Exception as e:
        print(f"Error processing cell {cell_name}: {e}")

if __name__ == "__main__":
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

        
        # # GMJULY2022
        # missing_ids = [i for i in range(50,60)]
        # missing_cells = [f'GMJULY2022_CELL{cell:03d}' for cell in missing_ids]  

        # missing_ids = [i for i in range(1,100)]
        # missing_cells = [f'UMBL2022FEB_CELL152{cell:03d}' for cell in missing_ids]

        # UMBL2022FEB
        # umbl_cell_nums_neware = [152057152046,152054,152045,152078,152097,152084,152085,152047, 152051,152087, 152036,152033,152088,152041,152094,152091,152048,152042,152039,152065,152072,
        # umbl_cell_nums_arbin = [152070, 152062, 152086, 152060, 152069,152061, 152093,152076,152052,152079,152089,152063,152068,152075,152055,152050,152067,152077,152059,152056,152058,152053,152082, 152066]
        # umbl_cell_nums = umbl_cell_nums_arbin #+ umbl_cell_nums_neware
        umbl_cell_nums = [152061, 152063, 152066]
        # umbl_cell_nums = [152042]#, 152039,] #
        missing_cells = [f'UMBL2022FEB_CELL{cell:03d}' for cell in umbl_cell_nums] 
        
        # missing_cells = ['LGM50T21700_CELL001']
        # missing_cells = ['LGM50_CELL003']
        # umbl_cell_nums = [2]
        # missing_cells = [f'GMFEB23D93_CELL{cell:03d}' for cell in umbl_cell_nums] 
        # missing_cells = ['GMFEB23D93_CELL002','GMFEB23D92_CELL009','GMFEB23D92_CELL002','GMFEB23D92_CELL007','GMFEB23D92_CELL004','GMFEB23D93_CELL001','GMFEB23D92_CELL003','GMFEB23D82_CELL004','GMFEB23D82_CELL007','GMFEB23D82_CELL006','GMFEB23D93_CELL009','GMFEB23D92_CELL001','GMFEB23D82_CELL010','GMFEB23D82_CELL003','GMFEB23D92_CELL003','GMFEB23D82_CELL005','GMFEB23D82_CELL002','GMFEB23D93_CELL008','GMFEB23D93_CELL005','GMFEB23D93_CELL013','GMFEB23D93_CELL004','GMFEB23D93_CELL012','GMFEB23D82_CELL001','GMFEB23D93_CELL007','GMFEB23D93_CELL006','GMFEB23D93_CELL010','GMFEB23D92_CELL005','GMFEB23D82_CELL009']
        # missing_cells = ['UMBL2022FEB_CELL151802','UMBL2022FEB_CELL151803','UMBL2022FEB_CELL151804','UMBL2022FEB_CELL151805','UMBL2022FEB_CELL151806']
        #missing_cells = ['LGM50LT_CELL004']

        missing_cells =[f'LGM50LT_CELL{cell:03d}' for cell in [4,17,18,19,35,36,37,38,39,40,41,42]]
        #missing_cells =[f'LGM50LT_CELL{cell:03d}' for cell in range(1,60)]
        #missing_cells = ['LGM50LT_CELL019']
        # umbl_cell_nums = [151802,151803,151804,151805,151806,152001,152002,152004,152005,152006,152007,152008,152009,152010,152011,152012,152013,152014,152015,152016,152017,152018,152019,152020,152021,152023,152026,152027,152028,152029,152030,152031,152032,152064,152071,152098]
        
        # umbl_cell_nums = [152002]
        # missing_cells = [f'UMBL2022FEB_CELL{cell:03d}' for cell in umbl_cell_nums] 

        # process project
        # project_name = 'GMJULY2022'
        # cell_service.process_cells_for_project(project_name=project_name, processor=processor, viewer=viewer)
        # missing_cells = [f'GMJULY2022_CELL{cell:03d}' for cell in [42]] 

        # with multiprocessing.Pool(processes=multiprocessing.cpu_count() - 3) as poo l:
        #     # Use the pool to process each cell in parallel
        #     pool.map(process_cell_in_parallel, missing_cells)
        # cell_service.process_cell('GMJULY2022_CELL042', processor, viewer)
        # cell_service.process_cell('GMJULY2022_CELL045', processor, viewer)
        # cell_service.process_cell('LGM50LT_CELL004', processor, viewer)
        # cell_service.process_cell('LGM50LT_CELL005', processor, viewer)
        # cell_service.process_cell('LGM50LT_CELL009', processor, viewer)
        
        # missing_cells = [f'LGM50LT_CELL{cell:03d}' for cell in range(10,46)] 
       # missing_cells = [f'GMFEB23S_CELL{cell:03d}' for cell in [19,55,11]] 
        # missing_cells = [f'LGM50LT_CELL{cell:03d}' for cell in [5,6,7,8,9,10,20,21,22]]
       # missing_cells = ['LGM50LT_CELL003','LGM50LT_CELL004','LGM50LT_CELL005','LGM50LT_CELL011']
        missing_cells = ['LGM50LT_CELL005']


        umbl_cell_nums = [19,55,11]
        missing_cells = [f'GMFEB23S_CELL{cell:03d}' for cell in umbl_cell_nums] 

      #  cell_service.process_cell('GMFEB23S_CELL019', processor, viewer)

        # run with progress bar
        with multiprocessing.Pool(processes = multiprocessing.cpu_count() - 3) as pool:
            results = []
            for result in tqdm(pool.imap_unordered(process_cell_in_parallel, missing_cells),
                            total=len(missing_cells),
                            desc="Processing cells",
                            unit="cell"):
                results.append(result)
