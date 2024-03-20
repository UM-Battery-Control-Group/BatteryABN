from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from .base import Base


class Project(Base):
    """
    Class for the test project. A project is a collection of cells.
    """

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    project_name = Column(String, unique=True)
    cells = relationship("Cell", back_populates="project")
    qmax = Column(Float)
    i_c20 = Column(Float)

    def get_qmax(self):
        """
        Get the total Qmax for the project.
        """
        return self.qmax

    def get_i_c20(self):
        """
        Get the total I_C20 for the project.
        """
        return self.i_c20
