from flask_injector import inject
from batteryabn import logger
from batteryabn.models import Project
from batteryabn.repositories import ProjectRepository, FileSystemRepository, create_project_repository, create_filesystem_repository

def create_project_service(session=None):
    project_repository = create_project_repository(session)
    filesystem_repository = create_filesystem_repository()
    return ProjectService(project_repository, filesystem_repository)

class ProjectService:
    """
    The ProjectService class provides an interface for creating and querying Project objects.
    """
    @inject
    def __init__(self, project_repository: ProjectRepository, file_system_repository: FileSystemRepository):
        self.project_repository = project_repository
        self.file_system_repository = file_system_repository

    def create_project(self, project_name: str) -> Project:
        """
        This method creates a new Project instance and adds it to the session.

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
        project = self.project_repository.find_by_name(project_name)
        if project:
            logger.info(f'Found existing project: {project_name}')
            return project

        # Project not found, so create a new one
        project = Project(project_name=project_name)
        self.project_repository.add(project)
        try:
            self.project_repository.commit()
            logger.info(f'Created new project: {project_name}')
        except Exception as e:
            self.project_repository.rollback()
            logger.error(f'Failed to create new project: {project_name}. Error: {e}')
            raise e
        return project
    
    def find_project_by_name(self, project_name: str):
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
        return self.project_repository.find_by_name(project_name)
    
    def get_all_projects(self):
        """
        This method returns all projects.

        Returns
        -------
        List[Project]
            A list of all projects
        """
        return self.project_repository.get_all_projects()
    
    def get_projects_in_filesystem(self):
        """
        This method returns all projects in the filesystem.

        Returns
        -------
        List[str]
            A list of all projects in the filesystem
        """
        return self.file_system_repository.get_projects_in_filesystem()