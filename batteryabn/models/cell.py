from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
import pickle

from batteryabn.utils import Utils
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
    project_name = Column(String, ForeignKey('projects.project_name'))
    project = relationship("Project", back_populates="cells")
    cell_data = Column(LargeBinary, nullable=True)
    cell_cycle_metrics = Column(LargeBinary, nullable=True)
    cell_data_vdf = Column(LargeBinary, nullable=True)
    # Images for the processed data
    image_cell = Column(LargeBinary, nullable=True)
    image_ccm = Column(LargeBinary, nullable=True)
    image_ccm_aht = Column(LargeBinary, nullable=True)


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
    
    def load_image_cell(self):
        """
        Load the cell image from the database.
        """
        return Utils.binary_to_image(self.image_cell)

    def load_image_ccm(self):
        """
        Load the cell cycle metrics image from the database.
        """
        return Utils.binary_to_image(self.image_ccm)
    
    def load_image_ccm_aht(self):
        """
        Load the cell cycle metrics AHT image from the database.
        """
        return Utils.binary_to_image(self.image_ccm_aht)