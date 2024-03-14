import pickle
from batteryabn import logger
from batteryabn.models import TestRecord, Cell
from batteryabn.repositories import CellRepository, TestRecordRepository
from batteryabn.utils import Processor


class CellService:
    """
    The CellService class provides an interface for creating and querying Cell objects.
    """
    def __init__(self, cell_repository: CellRepository, test_record_repository: TestRecordRepository):
        self.cell_repository = cell_repository
        self.test_record_repository = test_record_repository

    def create_cell(self, cell_name: str):
        """
        This method creates a new Cell instance and adds it to the session.

        Parameters
        ----------
        cell_name : str
            The unique name of the cell.

        Returns
        -------
        Cell
            The newly created Cell object
        """
        cell = self.cell_repository.find_by_name(cell_name)
        if not cell:
            cell = self.cell_repository.create_cell(cell_name)
            logger.info(f'Created new cell: {cell_name}')
        else:
            logger.info(f'Found existing cell: {cell_name}')
        return cell

    def find_cell_by_name(self, cell_name: str):
        """
        This method finds a Cell by its name.

        Parameters
        ----------
        cell_name : str
            The name of the cell to find

        Returns
        -------
        Cell
            The Cell object with the specified name
        """
        return self.cell_repository.find_by_name(cell_name)
    
    def process_cell(self, cell_name: str, processor: Processor):
        """
        Process cell data and save it to the database.

        Parameters
        ----------
        cell : Cell
            The cell to process
        processor : Processor
            Processor object with processed cell data
        """
        cell = self.find_cell_by_name(cell_name)

        if not cell:
            logger.error(f'Cell not found: {cell_name}')
            return
        
        cycler_trs, vdf_trs = self.get_cycler_vdf_trs(cell)
        processor.process(cycler_trs, vdf_trs)
        self.cell_repository.save_processed_data(cell, processor)

    def get_cycler_vdf_trs(self, cell: Cell):
        """
        Get cycler and Vdf test records for a cell.

        Parameters
        ----------
        cell : Cell
            The cell to get test records for

        Returns
        -------
        list
            Cycler test records
        list
            Vdf test records
        """
        trs = self.test_record_repository.find_by_cell_name(cell.cell_name)
        cycler_trs, vdf_trs = [], []
        for tr in trs:
            if tr.test_type == 'Neware_Vdf':
                vdf_trs.append(tr)
            else:
                cycler_trs.append(tr)
        return cycler_trs, vdf_trs
