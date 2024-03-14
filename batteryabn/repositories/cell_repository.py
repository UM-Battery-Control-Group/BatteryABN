import pickle
from sqlalchemy.orm import Session
from batteryabn.models import Cell
from batteryabn.utils import Processor
from batteryabn import logger



class CellRepository:
    """
    The CellRepository class provides an interface for querying and creating Cell objects.
    """
    def __init__(self, session: Session):
        self.session = session

    def find_by_name(self, cell_name: str):
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
        return self.session.query(Cell).filter_by(cell_name=cell_name).first()

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
        cell = Cell(cell_name=cell_name)
        self.session.add(cell)
        return cell
    
    def save_processed_data(self, cell: Cell, processor: Processor):
        """
        Save processed cell data to the database.

        Parameters
        ----------
        cell : Cell
            The cell to save processed data for
        processor : Processor
            Processor object with processed cell data
        """
        cell.cell_data = pickle.dumps(processor.cell_data)
        cell.cell_cycle_metrics = pickle.dumps(processor.cell_cycle_metrics)
        cell.cell_data_vdf = pickle.dumps(processor.cell_data_vdf)
        cell.cell_data_rpt = pickle.dumps(processor.cell_data_rpt)

        try:
            self.session.commit()
            logger.info(f'Saved processed data for cell: {cell.cell_name}')
        except Exception as e:
            self.session.rollback()
            raise e
