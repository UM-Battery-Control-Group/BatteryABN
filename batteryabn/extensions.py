from flask_sqlalchemy import SQLAlchemy
from flask_rq2 import RQ

# SQLAlchemy
db = SQLAlchemy()
# RQ
rq = RQ()