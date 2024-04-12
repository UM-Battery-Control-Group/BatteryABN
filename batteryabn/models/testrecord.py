import pickle
import pandas as pd
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, BIGINT
from sqlalchemy.orm import relationship

from batteryabn import Constants
from batteryabn.utils import Utils
from .base import Base


class TestRecord(Base):

    """
    Class for storing battery test data.

    Attributes
    ----------
    id : int
        Primary key
    test_name : str
        Name of the battery test
    test_type : str
        Type of the battery test, e.g. 'Arbin', 'BioLogic', 'Neware', 'Vdf'
    test_data : pickle
        Pickled test dataframe
    test_metadata : pickle
        Pickled test metadata dictionary
    """
    __tablename__ = 'testrecords'

    id = Column(Integer, primary_key=True)
    test_name = Column(String, unique=True)
    test_type = Column(String)
    cell_name = Column(String, ForeignKey('cells.cell_name'))
    # Store test data as pickled object
    test_data = Column(LargeBinary) 
    test_metadata = Column(LargeBinary)
    last_update_time = Column(BIGINT) # Unix timestamp
    cell = relationship("Cell", back_populates="test_records")


    def get_test_data(self) -> pd.DataFrame:
        """
        Get test data as dataframe.

        Returns
        -------
        pd.DataFrame
            Test data
        """
        return Utils.gzip_pickle_load(self.test_data)
    
    def get_test_metadata(self) -> dict:
        """
        Get test metadata as dictionary.

        Returns
        -------
        dict
            Test metadata
        """
        return Utils.gzip_pickle_load(self.test_metadata)
    
    def get_cycle_type(self) -> str:
        """
        Get the cycle type of the test. i.e. 'CYC', 'RPT', 'Test11', 'EIS', 'CAL', '_F' 

        Returns
        -------
        str
            Cycle type
        """
        # TODO: CYCLE_TYPES should be in the configuration file? 
        for type in Constants.CYCLE_TYPES:
            if type.lower() in self.test_name:
                return type
        # Default  
        return Constants.CYCLE_TYPES[0]
    
    def get_calibration_parameters(self):
        """
        Get calibration parameters for the test.

        Returns
        -------
        x1 : float
            Calibration parameter 1
        x2 : float
            Calibration parameter 2
        c : float
            Calibration parameter 3
        """
        # TODO: Implement calibration parameters.
        # It should associate the test with the cell and test time to get the calibration parameters
        # Temporarily return some default values
        return 1.6473, -27.134, 138.74
    
    def is_rpt(self) -> bool:
        """
        Check if the test is a RPT test.

        Returns
        -------
        bool
            True if the test is a RPT test, False otherwise
        """
        return 'rpt' in self.test_name.lower()
    
    def is_format(self) -> bool:
        """
        Check if the test is a formation test.

        Returns
        -------
        bool
            True if the test is a formation test, False otherwise
        """
        return '_f_' in self.test_name.lower()