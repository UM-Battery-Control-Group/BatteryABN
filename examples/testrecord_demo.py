import os
from batteryabn.repositories import TestRecordRepository, CellRepository, ProjectRepository
from batteryabn.services import TestRecordService
from batteryabn.utils import Parser, Formatter
from batteryabn.app import create_app
from batteryabn.models import db

current_directory = os.path.dirname(__file__)
calibration_parameters_path = '/home/me-bcl/Lab_share_Volt/voltaiq_data/sanity_check.csv'

app = create_app()

with app.app_context():
    db.create_all()

    parser = Parser()
    formatter = Formatter()
    cell_repository = CellRepository()
    test_record_repository = TestRecordRepository()
    project_repository = ProjectRepository()
    test_record_service = TestRecordService(cell_repository, test_record_repository, project_repository)

    parser.parse_calibration_parameters('/home/me-bcl/Lab_share_Volt/voltaiq_data/sanity_check.csv')
    formatter.format_calibration_parameters(parser.calibration_parameters)

    cells = [f"GMFEB23S_CELL{str(i).zfill(3)}" for i in [70, 73]]
    for cell in cells:
        data_directory = f'/home/me-bcl/Lab_share_Volt/PROJ_GMFEB23S/Cycler_Data_By_Cell/{cell}'
        test_record_service.create_and_save_trs(data_directory, key_word='GMFEB23S', parser=parser, formatter=formatter, reset=True)

    # cells = [f"GMJuly2022_CELL{str(i).zfill(3)}" for i in range(21, 22)] #59, 67, 69
    # for cell in cells:
    #     data_directory = f'/home/me-bcl/Lab_share_Volt/PROJ_GMJULY2022/Cycler_Data_By_Cell/{cell}'
    #     test_record_service.create_and_save_trs(data_directory, key_word='GMJuly2022', parser=parser, formatter=formatter, reset=True)





