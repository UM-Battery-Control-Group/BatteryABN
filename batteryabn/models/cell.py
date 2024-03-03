from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

from batteryabn import logger
from .base import Base

class Cell(Base):
    """
    Class for storing battery cell data.
    """

    __tablename__ = 'cells'

    id = Column(Integer, primary_key=True)
    # Unique cell name. i.e. 'GMJuly2022_CELL002'
    cell_name = Column(String, unique=True) 

    test_records = relationship("TestRecord", back_populates="cell")

def create_cell(cell_name):
    """
    Factory function to create a new Cell instance.

    Parameters
    ----------
    cell_name : str
        The unique name of the cell.

    Returns
    -------
    Cell
        A new Cell instance with the specified cell name.
    """
    return Cell(cell_name=cell_name)

    
