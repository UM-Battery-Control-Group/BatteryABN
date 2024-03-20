from batteryabn.models import Project
from .base_repository import BaseRepository


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
