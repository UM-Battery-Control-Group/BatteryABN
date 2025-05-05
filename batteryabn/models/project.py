from batteryabn import Constants as Const
from ..extensions import db


class Project(db.Model):
    """
    Class for the test project. A project is a collection of cells.
    """

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, unique=True)
    cells = db.relationship("Cell", back_populates="project")
    qmax = db.Column(db.Float)
    i_c20 = db.Column(db.Float)

    def get_qmax(self):
        """
        Get the total Qmax for the project.
        """
        return self.qmax if self.qmax else Const.QMAX

    def get_i_c20(self):
        """
        Get the total I_C20 for the project.
        """
        return self.i_c20

    def to_dict(self):
        """
        Convert the Project object to a dictionary.
        """
        return {
            'project_name': self.project_name,
            'qmax': self.get_qmax(),
            'i_c20': self.get_i_c20()
        }