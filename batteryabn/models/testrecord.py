import pandas as pd
from batteryabn import Constants
from batteryabn.utils import Utils
from ..extensions import db


class TestRecord(db.Model):

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

    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String)
    test_type = db.Column(db.String)
    cell_name = db.Column(db.String, db.ForeignKey('cells.cell_name'))
    # Store test data as pickled object
    test_data = db.Column(db.LargeBinary) 
    test_metadata = db.Column(db.LargeBinary)
    start_time = db.Column(db.BIGINT, nullable=True)  # Unix timestamp
    last_update_time = db.Column(db.BIGINT)  # Unix timestamp
    size = db.Column(db.Integer, nullable=True)  # Size of the test data in bytes
    # Relationship with the Cell model
    cell = db.relationship("Cell", back_populates="test_records")


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
            if type.upper() in self.test_name:
                return type
        # Default  
        return Constants.CYCLE_TYPES[0]
    
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
    
    def to_dict(self) -> dict:
        """
        Convert the TestRecord object to a dictionary.

        Returns
        -------
        dict
            Test record dictionary
        """
        return {
            'test_name': self.test_name,
            'test_type': self.test_type,
            'cell_name': self.cell_name,
            'start_time': self.start_time,
            'last_update_time': self.last_update_time
        }