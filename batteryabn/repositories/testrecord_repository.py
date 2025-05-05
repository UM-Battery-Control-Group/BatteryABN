from batteryabn.models import TestRecord
from .base_repository import BaseRepository

def create_test_record_repository(session=None):
    return TestRecordRepository(session)

class TestRecordRepository(BaseRepository):
    """
    The TestRecordRepository class provides an interface for saving and querying TestRecord objects.
    """

    def find_by_name(self, test_name: str, test_type: str):
        return self.session.query(TestRecord).filter_by(test_name=test_name, test_type=test_type).first()
    
    def find_by_cell_name(self, cell_name: str):
        return self.session.query(TestRecord).filter_by(cell_name=cell_name.upper()).all()
    
    def find_by_keyword(self, keyword: str):
        return self.session.query(TestRecord).filter(TestRecord.test_name.ilike(f'%{keyword}%')).all()