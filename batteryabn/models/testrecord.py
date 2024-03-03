import pickle
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship, Session


from batteryabn.utils.parser import Parser
from batteryabn.utils.formatter import Formatter
from batteryabn import logger
from .base import Base
from .cell import Cell, create_cell

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
    test_name = Column(String)
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

    def save_to_db(self, session: Session):
        """
        Save test record to database.

        Parameters
        ----------
        session : Session
            SQLAlchemy session
        """
        cell = session.query(Cell).filter_by(cell_name=self.cell_name).first()
        if not cell:
            # If no existing Cell, create a new one.
            logger.info(f'Creating new cell: {self.cell_name}')
            cell = create_cell(self.cell_name)
            session.add(cell)
        else:
            logger.info(f'Found existing cell: {self.cell_name}')
        
        # Associate this TestRecord with the found or new Cell
        self.cell = cell

        # Add TestRecord to the session and commit
        session.add(self)
        session.commit()
        logger.info(f'Saved test record: {self.test_name} to database')

def create_test_record(path: str, parser: Parser, formatter: Formatter, session: Session):
    """
    Factory function to create a new TestRecord instance, load test data from file, and save to database.

    Parameters
    ----------
    path : str
        Path to battery test data file
    parser : Parser
        Parser object to parse test data
    formatter : Formatter
        Formatter object to format test data
    session : Session
        SQLAlchemy session

    Returns
    -------
    TestRecord
        A new TestRecord instance with the specified test data.
    """
    test_record = TestRecord()
    test_record.load_from_file(path, parser, formatter)
    test_record.save_to_db(session)
    return test_record
