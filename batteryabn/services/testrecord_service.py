from batteryabn import logger
from batteryabn.models import TestRecord
from batteryabn.utils import Parser, Formatter
from batteryabn.repositories import CellRepository, TestRecordRepository


class TestRecordService:
    """
    The TestRecordService class provides an interface for saving TestRecord objects.
    """
    def __init__(self, cell_repository: CellRepository, test_record_repository: TestRecordRepository):
        self.cell_repository = cell_repository
        self.test_record_repository = test_record_repository

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
        test_record = TestRecord()
        test_record.load_from_file(path, parser, formatter)
        # Check if the test record already exists in the database
        tr_in_db = self.find_test_record_by_name(parser.test_name)
        # TODO: Check if the test record should be updated if it already exists
        # Now, we just skip saving the test record if it already exists
        if tr_in_db:
            logger.info(f'Test record already exists: {parser.test_name}')
            return
        cell_name = formatter.cell_name
        cell = self.cell_repository.find_by_name(cell_name)
        if not cell:
            logger.info(f'Creating new cell: {cell_name}')
            cell = self.cell_repository.create_cell(cell_name)
        else:
            logger.info(f'Found existing cell: {cell_name}')
        
        test_record.cell = cell
        self.test_record_repository.save(test_record)
        logger.info(f'Saved test record: {test_record.test_name} to database')

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
