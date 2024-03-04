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

    
