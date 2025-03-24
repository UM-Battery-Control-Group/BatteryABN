from flask_injector import inject
from batteryabn import logger, Constants as Const
from batteryabn.models import TestRecord, Cell, Project
from batteryabn.utils import Parser, Formatter, Utils
from batteryabn.repositories import CellRepository, TestRecordRepository, ProjectRepository
from batteryabn.repositories import create_cell_repository, create_test_record_repository, create_project_repository


def create_test_record_service(session=None):
    cell_repository = create_cell_repository(session)
    test_record_repository = create_test_record_repository(session)
    project_repository = create_project_repository(session)
    return TestRecordService(cell_repository, test_record_repository, project_repository)

class TestRecordService:
    """
    The TestRecordService class provides an interface for saving TestRecord objects.
    """
    @inject
    def __init__(self, cell_repository: CellRepository, test_record_repository: TestRecordRepository, project_repository: ProjectRepository):
        self.cell_repository = cell_repository
        self.test_record_repository = test_record_repository
        self.project_repository = project_repository

    def create_and_save_tr(self, path: str, parser: Parser, formatter: Formatter, reset: bool = False):
        """
        This method creates a new TestRecord and saves it to the database. 
        If the cell associated with the test record does not exist, it is created.

        Parameters
        ----------
        path : str
            Path to battery test data file
        parser : Parser
            Parser object to parse test data
        formatter : Formatter
            Formatter object to format test data
        reset : bool, optional
            If True, the test record will be created even if it already exists, by default False
        """
        logger.info(f'Creating new test record from file: {path}')
        parser.parse(path)

        test_name = parser.test_name
        test_type = parser.test_type
        test_record = self.test_record_repository.find_by_name(test_name, test_type)

        # Check if the test record exists and size is up-to-date
        if not reset and test_record:
            size_is_valid = (
                test_record.size is not None and
                parser.test_size is not None and
                test_record.size >= parser.test_size
            )
            if size_is_valid:
                logger.info(f'Test record already exists and size is up-to-date: {test_name}')
                return

        # Process the data (formatter needs to run before checking time)
        formatter.format_data(parser.raw_test_data, parser.raw_metadata, parser.test_type)

        # Check if the test record's last update time is up-to-date
        if not reset and test_record:
            time_is_valid = (
                test_record.last_update_time is not None and
                formatter.last_update_time is not None and
                test_record.last_update_time >= formatter.last_update_time
            )
            if time_is_valid:
                logger.info(f'Test record already exists and is up-to-date: {test_name}')
                return

        # Check if cell exists, if not create it
        cell = self.cell_repository.find_by_name(formatter.cell_name)
        if not cell:
            logger.info(f'Creating new cell: {formatter.cell_name}')
            cell = Cell(cell_name=formatter.cell_name)
            self.cell_repository.add(cell)

        # Create or update the test record
        if not test_record:
            test_record = TestRecord(test_name=test_name, test_type=test_type)
            self.test_record_repository.add(test_record)

        # Load data from parser and formatter
        test_record.size = parser.test_size
        test_record.cell_name = formatter.cell_name
        test_record.test_data = Utils.gzip_pikle_dump(formatter.test_data)
        test_record.test_metadata = Utils.gzip_pikle_dump(formatter.metadata)
        test_record.last_update_time = formatter.last_update_time
        test_record.cell = cell
        logger.info(f'Saving test record: {test_name}')

        # Check if project exists, if not create it
        project_name = formatter.metadata.get('Project Name')
        if project_name:
            project = self.project_repository.find_by_name(project_name)
            if not project:
                logger.info(f'Creating new project: {project_name}')
                project = Project(project_name=project_name)
                self.project_repository.add(project)
            # Associate the cell with the project.
            cell.project = project
        
        try:
            self.test_record_repository.commit()
            logger.info(f'Saved test record: {test_name} to database')
        except Exception as e:
            self.test_record_repository.rollback()
            logger.error(f'Failed to save test record: {test_name}. Error: {e}')
            raise e

    def create_and_save_trs(self, path: str, key_word: str, parser: Parser, formatter: Formatter, 
                            file_extensions: list[str] = Const.FILE_TYPE_2_TEST_TYPE.keys(), reset: bool = False):
        """
        Create and save TestRecords from a list of files.

        Parameters
        ----------
        paths : str
            Root directory to search for files
        key_word : str
            Keyword to search for in file names
        parser : Parser
            Parser object to parse test data
        formatter : Formatter
            Formatter object to format test data
        file_extensions : list[str], optional
            List of file extensions to search for, by default ['.xlsx', '.csv', '.mpr']
        reset : bool, optional
            If True, the test record will be created even if it already exists, by default False        
        """

        files = Utils.search_files(path, key_word, file_extensions)
        for file in files:
            self.create_and_save_tr(file, parser, formatter, reset)

    def find_test_record_by_name(self, test_name: str, test_type: str):
        """
        This method finds a TestRecord by its name.

        Parameters
        ----------
        test_name : str
            The name of the test record to find
        test_type : str
            The type of the test record to find

        Returns
        -------
        TestRecord
            The TestRecord object with the specified name
        """
        return self.test_record_repository.find_by_name(test_name, test_type)
    
    def find_test_records_by_cell_name(self, cell_name: str):
        """
        This method finds all TestRecords associated with a Cell.

        Parameters
        ----------
        cell_name : str
            The name of the cell

        Returns
        -------
        List[TestRecord]
            A list of TestRecord objects associated with the specified cell
        """
        return self.test_record_repository.find_by_cell_name(cell_name)
    
    def find_test_records_by_keyword(self, keyword: str):
        """
        This method finds all TestRecords that match a keyword.

        Parameters
        ----------
        keyword : str
            The keyword to search for

        Returns
        -------
        List[TestRecord]
            A list of TestRecord objects that match the keyword
        """
        return self.test_record_repository.find_by_keyword(keyword)


    def delete_test_record(self, test_name: str, test_type: str):
        """
        This method deletes a TestRecord from the database.

        Parameters
        ----------
        test_name : str
            The name of the test record to delete
        test_type : str
            The type of the test record to delete
        """
        test_record = self.test_record_repository.find_by_name(test_name, test_type)
        if test_record:
            self.test_record_repository.delete(test_record)
            self.test_record_repository.commit()
            logger.info(f'Deleted test record: {test_name}')
        else:
            logger.info(f'Test record not found: {test_name}')

    def delete_test_records_by_cell_name(self, cell_name: str):
        """
        This method deletes all TestRecords associated with a Cell.

        Parameters
        ----------
        cell_name : str
            The name of the cell
        """
        test_records = self.test_record_repository.find_by_cell_name(cell_name)
        for test_record in test_records:
            self.test_record_repository.delete(test_record)
        self.test_record_repository.commit()
        logger.info(f'Deleted test records associated with cell: {cell_name}')