from sqlalchemy.orm import Session
from batteryabn.models import Project

from batteryabn import logger



class ProjectRepository:
    """
    The ProjectRepository class provides an interface for saving and querying Project objects.
    """
    def __init__(self, session: Session):
        self.session = session

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

    def create_project(self, project_name: str):
        """
        This method creates a new Project instance and adds it to the session.
        All project names are unique and should be uppercase.

        Parameters
        ----------
        project_name : str
            The unique name of the project.

        Returns
        -------
        Project
            The newly created Project object
        """
        project_name = project_name.upper()
        project = self.find_by_name(project_name)
        if not project:
            project = Project(project_name=project_name)
            self.session.add(project)
            logger.info(f'Created new project: {project_name}')
        else:
            logger.info(f'Found existing project: {project_name}')
        return project