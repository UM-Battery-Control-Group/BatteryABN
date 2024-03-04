from sqlalchemy.orm import Session
from batteryabn.models import Cell

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