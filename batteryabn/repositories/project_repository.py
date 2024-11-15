from batteryabn.models import Project
from .base_repository import BaseRepository

def create_project_repository():
    return ProjectRepository()

class ProjectRepository(BaseRepository):
    """
    The ProjectRepository class provides an interface for saving and querying Project objects.
    """

    def find_by_name(self, project_name: str):
        """
        This method finds a Project by its name.

        Parameters
        ----------
        project_name : str
            The name of the project to find

        Returns
        -------
        Project
            The Project object with the specified name
        """
        return self.session.query(Project).filter_by(project_name=project_name.upper()).first()

    def get_all_projects(self):
        """
        This method returns all projects in the database.

        Returns
        -------
        List[Project]
            A list of all Project objects in the database
        """
        return self.session.query(Project).all()