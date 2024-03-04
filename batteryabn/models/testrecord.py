import pickle
import pandas as pd
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship, Session


from batteryabn.utils.parser import Parser
from batteryabn.utils.formatter import Formatter
from batteryabn import logger
from .base import Base
from .cell import Cell

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
        Type of the battery test, e.g. 'Arbin', 'BioLogic', 'Neware', 'Neware_Vdf'
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
    cell = relationship("Cell", back_populates="test_records")

    def load_from_file(self, path: str, parser: Parser, formatter: Formatter):
        """
        Load battery test data from file.

        Parameters
        ----------
        path : str
            Path to battery test data file
        parser : Parser
            Parser object to parse test data
        formatter : Formatter
            Formatter object to format test data
        """
        parser.parse(path)
        formatter.format_data(parser.raw_test_data, parser.raw_metadata, parser.test_type)
        self.test_name = parser.test_name
        self.test_type = parser.test_type
        self.cell_name = formatter.cell_name
        self.test_data = pickle.dumps(formatter.test_data)
        self.test_metadata = pickle.dumps(formatter.metadata)
        logger.debug(f'Loaded test data from file: {path}')

    def get_test_data(self) -> pd.DataFrame:
        """
        Get test data as dataframe.

        Returns
        -------
        pd.DataFrame
            Test data
        """
        return pickle.loads(self.test_data)
    
    def get_test_metadata(self) -> dict:
        """
        Get test metadata as dictionary.

        Returns
        -------
        dict
            Test metadata
        """
        return pickle.loads(self.test_metadata)