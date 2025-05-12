import os
import pytest
import pandas as pd
import pickle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from batteryabn.models import TestRecord, Cell
from batteryabn.repositories import TestRecordRepository, CellRepository
from batteryabn.services import TestRecordService

from batteryabn.utils import Parser, Formatter
from batteryabn.models.base import Base

BASE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
NEWARE_PATH = os.path.join(BASE_DATA_PATH, 'neware')
NEWARE_VDF_PATH = os.path.join(BASE_DATA_PATH, 'neware_vdf')



@pytest.fixture(scope="module")
def db_session():
    # Use an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Create the tables
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_test_record_integration(db_session):
    parser = Parser()
    formatter = Formatter()
    cell_repository = CellRepository(db_session)
    test_record_repository = TestRecordRepository(db_session)
    test_record_service = TestRecordService(cell_repository, test_record_repository)

    paths = [
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_RPT_3_P0C_5P0PSI_20230110_R0_CH041_20230110143333_37_2_1_2818580185.xlsx'),
        os.path.join(NEWARE_PATH, 'GMJuly2022_CELL002_Test3_1_P0C_5P0PSI_20221115_R0_CH041_20221115074501_37_2_1_2818580175_1.xlsx'),
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R0_CH041.csv'),
        os.path.join(NEWARE_VDF_PATH, 'GMJuly2022_CELL002_RPT_1_P0C_5P0PSI_20221011_R1_CH041.csv'),
    ]

    for path in paths:
        test_record_service.create_and_save_tr(path, parser, formatter)

    # Check that the test records were added to the database
    test_records = db_session.query(TestRecord).all()
    assert len(test_records) == 4
    for test_record in test_records:
        assert test_record.cell_name == 'GMJuly2022_CELL002'
        assert test_record.test_name is not None
        assert test_record.test_data is not None
        assert test_record.test_metadata is not None
        assert test_record.test_type in ['Neware', 'Neware_Vdf']

    # Check that the cell was added to the database
    cell = db_session.query(Cell).filter_by(cell_name='GMJuly2022_CELL002').first()
    assert cell is not None
