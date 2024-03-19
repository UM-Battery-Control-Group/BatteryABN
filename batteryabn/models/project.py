from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from batteryabn import logger
from .base import Base

class Project(Base):
    """
    Class for the test project. A project is a collection of cells.
    """

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    project_name = Column(String, unique=True)
    cells = relationship("Cell", back_populates="project")

