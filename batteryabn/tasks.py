import os
from redis import Redis
from rq import Queue, Worker, Connection
from dotenv import load_dotenv

load_dotenv(dotenv_path='dev.env')
REDIS_URL = os.getenv('REDIS_URL')

redis_conn = Redis.from_url(REDIS_URL)
task_queue = Queue(connection=redis_conn)

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker([task_queue]) 
        worker.work()
