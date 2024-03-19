from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
import pickle

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
    project = relationship("Project", back_populates="cells")
    cell_data = Column(LargeBinary, nullable=True)
    cell_cycle_metrics = Column(LargeBinary, nullable=True)
    cell_data_vdf = Column(LargeBinary, nullable=True)
    cell_data_rpt = Column(LargeBinary, nullable=True)

    def load_cell_data(self):
        """
        Load cell data from the database.
        """
        return pickle.loads(self.cell_data)
    
    def load_cell_cycle_metrics(self):
        """
        Load cell cycle metrics from the database.
        """
        return pickle.loads(self.cell_cycle_metrics)
    
    def load_cell_data_vdf(self):
        """
        Load cell VDF data from the database.
        """
        return pickle.loads(self.cell_data_vdf)

    def load_cell_data_rpt(self):
        """
        Load cell RPT data from the database.
        """
        return pickle.loads(self.cell_data_rpt)    
