from batteryabn.models import Cell
from .base_repository import BaseRepository


class CellRepository(BaseRepository):
    """
    The CellRepository class provides an interface for querying and creating Cell objects.
    """

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
        return self.session.query(Cell).filter_by(cell_name=cell_name.upper()).first()

    def find_by_project(self, project_name: str):
        """
        This method finds all Cells in a Project.

        Parameters
        ----------
        project_name : str
            The name of the project to find cells for

        Returns
        -------
        list
            A list of Cell objects in the specified project
        """
        return self.session.query(Cell).filter_by(project_name=project_name.upper()).all()
    
    def find_by_keyword(self, keyword: str):
        """
        This method finds all Cells that match a keyword.

        Parameters
        ----------
        keyword : str
            The keyword to search for

        Returns
        -------
        list
            A list of Cell objects that match the keyword
        """
        return self.session.query(Cell).filter(Cell.cell_name.ilike(f'%{keyword}%')).all()