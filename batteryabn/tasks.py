from flask import current_app
from sqlalchemy.orm import sessionmaker
from .extensions import db, rq
from .services import create_cell_service, create_test_record_service
from .utils import create_processor, create_viewer, create_parser, create_formatter


@rq.job
def process_cell_task(cell_name: str):
    """
    Function called by the task queue to process a cell by its name.
    """
    with current_app.app_context():
        engine = db.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            cell_service = create_cell_service(session=session)
            processor = create_processor()
            viewer = create_viewer()
            cell_service.process_cell(cell_name, processor, viewer)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return

@rq.job
def update_trs_task(data_directory: str, cell_name: str, reset: bool):
    """
    Function called by the task queue to update test records for a cell by its name.
    """
    with current_app.app_context():
        engine = db.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            test_record_service = create_test_record_service(session=session)
            parser = create_parser()
            formatter = create_formatter()
            test_record_service.create_and_save_trs(data_directory, cell_name, parser, formatter, reset=reset)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return
