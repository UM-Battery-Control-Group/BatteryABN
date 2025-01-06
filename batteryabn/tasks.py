from flask import current_app
from sqlalchemy.orm import sessionmaker
from rq.job import Job
from .extensions import db, rq
from .services import create_cell_service, create_test_record_service
from .utils import create_processor, create_viewer, create_parser, create_formatter


@rq.job(timeout=60 * 60)
def process_cell_task(cell_name: str):
    """
    Function called by the task queue to process a cell by its name.
    """
    with current_app.app_context():
        engine = db.get_engine()
        Session = sessionmaker(bind=engine)
        with Session() as session:
            try:
                cell_service = create_cell_service(session=session)
                processor = create_processor()
                viewer = create_viewer()
                cell_service.process_cell(cell_name, processor, viewer)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
    return

@rq.job(timeout=60 * 60)
def update_trs_task(data_directory: str, cell_name: str, reset: bool):
    """
    Function called by the task queue to update test records for a cell by its name.
    """
    with current_app.app_context():
        engine = db.get_engine()
        Session = sessionmaker(bind=engine)
        with Session() as session:
            try:
                test_record_service = create_test_record_service(session=session)
                parser = create_parser()
                formatter = create_formatter()
                test_record_service.create_and_save_trs(data_directory, cell_name, parser, formatter, reset=reset)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
    return


def get_tasks_status():
    queue = rq.get_queue()
    started_registry = queue.started_job_registry
    finished_registry = queue.finished_job_registry
    failed_registry = queue.failed_job_registry
    def fetch_job_details(job_id):
        job = queue.fetch_job(job_id)
        if job is None:
            return {"id": job_id, "status": "unknown"}
        return {
            "id": job.id,
            "status": job.get_status(),
            "enqueued_at": job.enqueued_at.strftime('%Y-%m-%d %H:%M:%S') if job.enqueued_at else None,
            "started_at": job.started_at.strftime('%Y-%m-%d %H:%M:%S') if job.started_at else None,
            "ended_at": job.ended_at.strftime('%Y-%m-%d %H:%M:%S') if job.ended_at else None,
            "description": job.description,
        }
    result = {
        "queued": [
            {
                "id": job.id,
                "status": job.get_status(),
                "enqueued_at": job.enqueued_at.strftime('%Y-%m-%d %H:%M:%S') if job.enqueued_at else None,
                "description": job.description,
            }
            for job in queue.jobs
        ],
        "started": [fetch_job_details(job_id) for job_id in started_registry.get_job_ids()],
        "finished": [fetch_job_details(job_id) for job_id in finished_registry.get_job_ids()],
        "failed": [fetch_job_details(job_id) for job_id in failed_registry.get_job_ids()],
    }
    return result

def clear_all():
    queue = rq.get_queue() 
    queue.empty()
    return {"status": "success", "message": "Cleared all tasks"}

def clear_finished():
    queue = rq.get_queue() 
    finished_registry = queue.finished_job_registry

    finished_job_ids = finished_registry.get_job_ids()

    for job_id in finished_job_ids:
        job = Job.fetch(job_id, connection=queue.connection)
        job.delete()
        finished_registry.remove(job_id)

    return {"status": "success", "message": f"Cleared {len(finished_job_ids)} finished tasks"}

def clear_failed():
    queue = rq.get_queue() 
    failed_registry = queue.failed_job_registry

    failed_job_ids = failed_registry.get_job_ids()

    for job_id in failed_job_ids:
        job = Job.fetch(job_id, connection=queue.connection)
        job.delete()
        failed_registry.remove(job_id)

    return {"status": "success", "message": f"Cleared {len(failed_job_ids)} failed tasks"}