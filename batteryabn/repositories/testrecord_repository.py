from sqlalchemy.orm import Session
from batteryabn.models import TestRecord

class TestRecordRepository:
    """
    The TestRecordRepository class provides an interface for saving and querying TestRecord objects.
    """
    def __init__(self, session: Session):
        self.session = session

    def save(self, test_record: TestRecord):
        """
        This method saves a TestRecord object to the database.

        Parameters
        ----------
        test_record : TestRecord
            TestRecord object to save
        """
        try:
            self.session.add(test_record)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def find_by_name(self, test_name: str):
        return self.session.query(TestRecord).filter_by(test_name=test_name).first()
    
    def find_by_cell_name(self, cell_name: str):
        return self.session.query(TestRecord).filter_by(cell_name=cell_name).all()