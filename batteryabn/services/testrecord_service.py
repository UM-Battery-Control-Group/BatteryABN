import pickle
from batteryabn import logger
from batteryabn.models import TestRecord, Cell, Project
from batteryabn.utils import Parser, Formatter
from batteryabn.repositories import CellRepository, TestRecordRepository, ProjectRepository


class TestRecordService:
    """
    The TestRecordService class provides an interface for saving TestRecord objects.
    """
    def __init__(self, cell_repository: CellRepository, test_record_repository: TestRecordRepository, project_repository: ProjectRepository):
        self.cell_repository = cell_repository
        self.test_record_repository = test_record_repository
        self.project_repository = project_repository

    def create_and_save_tr(self, path: str, parser: Parser, formatter: Formatter):
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
        """
        logger.info(f'Creating new test record from file: {path}')
        parser.parse(path)
        formatter.format_data(parser.raw_test_data, parser.raw_metadata, parser.test_type)

        test_name = parser.test_name
        test_record = self.test_record_repository.find_by_name(test_name)

        # If test record exists and is up-to-date, no action needed
        if test_record and test_record.last_update_time >= formatter.last_update_time:
            logger.info(f'Test record already exists and is up-to-date: {test_name}')
            return

        # Create or update the test record
        if not test_record:
            test_record = TestRecord(test_name=test_name)
            self.test_record_repository.add(test_record)

        # Load data from parser and formatter
        test_record.test_type = parser.test_type
        test_record.cell_name = formatter.cell_name
        test_record.test_data = pickle.dumps(formatter.test_data)
        test_record.test_metadata = pickle.dumps(formatter.metadata)
        test_record.last_update_time = formatter.last_update_time

        # Check if cell exists, if not create it
        cell = self.cell_repository.find_by_name(formatter.cell_name)
        if not cell:
            logger.info(f'Creating new cell: {formatter.cell_name}')
            cell = Cell(cell_name=formatter.cell_name)
            self.cell_repository.add(cell)
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


    def find_test_record_by_name(self, test_name: str):
        """
        This method finds a TestRecord by its name.

        Parameters
        ----------
        test_name : str
            The name of the test record to find

        Returns
        -------
        TestRecord
            The TestRecord object with the specified name
        """
        return self.test_record_repository.find_by_name(test_name)
    
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
