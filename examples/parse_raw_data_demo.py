import multiprocessing
import os
from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository
from batteryabn.services import TestRecordService
from batteryabn.utils import Parser, Formatter
from batteryabn.app import create_app
from batteryabn.extensions import db
from tqdm import tqdm

current_directory = os.path.dirname(__file__)
calibration_parameters_path = './sanity_check.csv'

def process_cell_in_parallel(cell_name):
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            data_directory = f'/data/'
           
            parser = Parser()
            formatter = Formatter()
            cell_repository = CellRepository()
            test_record_repository = TestRecordRepository()
            project_repository = ProjectRepository()
            test_record_service = TestRecordService(cell_repository, test_record_repository, project_repository)

            parser.parse_calibration_parameters(calibration_parameters_path)
            formatter.format_calibration_parameters(parser.calibration_parameters)
            test_record_service.create_and_save_trs(data_directory, key_word=cell_name, parser=parser, formatter=formatter,  reset=True)#,file_extensions=['csv'],

    except Exception as e:
        print(f"Error processing cell {cell_name}: {e}")

if __name__ == "__main__":
    app = create_app()

with app.app_context():
    db.create_all()

    parser = Parser()
    formatter = Formatter()
    cell_repository = CellRepository()
    test_record_repository = TestRecordRepository()
    project_repository = ProjectRepository()
    test_record_service = TestRecordService(cell_repository, test_record_repository, project_repository)

    parser.parse_calibration_parameters(calibration_parameters_path)
    formatter.format_calibration_parameters(parser.calibration_parameters)

    data_directory = f'/data/'
    key_word ='UMBL2022FEB_CELL152052'
    key_word ='GMJULY2022_CELL042'
    missing_ids = [i for i in range(1,121)]
    cellNames = [f'GMJULY2022_CELL{cell:03d}' for cell in missing_ids]
    
    missing_ids = [i for i in range(1,100)]
    cellNames = [f'UMBL2022FEB_CELL152{cell:03d}' for cell in missing_ids]


    umbl_cell_nums = [152042]
    umbl_cell_nums = [152001]
    cellNames = [f'UMBL2022FEB_CELL{cell:03d}' for cell in umbl_cell_nums] 
    umbl_cell_nums = [2]
    cellNames = [f'GMFEB23D93_CELL{cell:03d}' for cell in umbl_cell_nums] 
    cellNames = ['GMFEB23D93_CELL002','GMFEB23D92_CELL009','GMFEB23D92_CELL002','GMFEB23D92_CELL007','GMFEB23D92_CELL004','GMFEB23D93_CELL001','GMFEB23D92_CELL003','GMFEB23D82_CELL004','GMFEB23D82_CELL007','GMFEB23D82_CELL006','GMFEB23D93_CELL009','GMFEB23D92_CELL001','GMFEB23D82_CELL010','GMFEB23D82_CELL003','GMFEB23D92_CELL003','GMFEB23D82_CELL005','GMFEB23D82_CELL002','GMFEB23D93_CELL008','GMFEB23D93_CELL005','GMFEB23D93_CELL013','GMFEB23D93_CELL004','GMFEB23D93_CELL012','GMFEB23D82_CELL001','GMFEB23D93_CELL007','GMFEB23D93_CELL006','GMFEB23D93_CELL010','GMFEB23D92_CELL005','GMFEB23D82_CELL009']
   # cellNames = ['UMBL2022FEB_CELL151802','UMBL2022FEB_CELL151803','UMBL2022FEB_CELL151804','UMBL2022FEB_CELL151805','UMBL2022FEB_CELL151806']

    umbl_cell_nums = [151802,151803,151804,151805,151806,152001,152002,152004,152005,152006,152007,152008,152009,152010,152011,152012,152013,152014,152015,152016,152017,152018,152019,152020,152021,152023,152026,152027,152028,152029,152030,152031,152032,152064,152071,152098]
    # umbl_cell_nums = [152001,152002,152004,152005]
    cellNames = [f'UMBL2022FEB_CELL{cell:03d}' for cell in umbl_cell_nums] 

    # cellNames = ['LGM50T21700_CELL001']

    # cellNames = ['LGM50LT_CELL005']

    # umbl_cell_nums = [19,55,11]
    # cellNames = [f'GMFEB23S_CELL{cell:03d}' for cell in umbl_cell_nums] 
    cellNames = [f'LGM50LT_CELL{cell:03d}' for cell in range(1,47)] #range(10,46)] 
    #cellNames=['LGM50LT_CELL005','LGM50LT_CELL006','LGM50LT_CELL007']
# 5,6,7,8,9,10,20,21,22
    #cellNames = [f'GMFEB23S_CELL{cell:03d}' for cell in [19,55,11]] 
    # cellNames = ['GMFEB23S_CELL020']

 #   for key_word in cellNames: 
#       test_record_service.create_and_save_trs(data_directory, key_word=key_word, parser=parser, formatter=formatter,  reset=True)#,file_extensions=['csv'],


    with multiprocessing.Pool(processes = multiprocessing.cpu_count() - 1) as pool:
            results = []
            for result in tqdm(pool.imap_unordered(process_cell_in_parallel, cellNames),
                            total=len(cellNames),
                            desc="Processing cells",
                            unit="cell"):
                results.append(result)

    # missing_ids = [i for i in range(1, 5)]
    # for cell in missing_ids:
    #     # data_directory = f'/data'
    #     # # data_directory = f'/home/me-bcl/Lab_share_Volt/PROJ_GMJULY2022/'
    #     # key_word = 'GMJULY2022' + '_CELL' + f'{cell:03d}'
    #     # test_record_service.create_and_save_trs(data_directory, key_word=key_word, parser=parser, formatter=formatter, reset=False)


    #     data_directory = f'/home/me-bcl/Lab_share_Volt/PROJ_SANDIA/'
    #     key_word = 'sandiaKokam' + '_CELL' + f'{cell:03d}'
    #     test_record_service.create_and_save_trs(data_directory, key_word=key_word, parser=parser, formatter=formatter, reset=False)
