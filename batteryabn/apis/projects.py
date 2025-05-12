from flask import Blueprint, jsonify
from flask_injector import inject
from batteryabn.services import ProjectService

projects_bp = Blueprint('projects', __name__)

@inject
@projects_bp.route('/', methods=['GET'])
def get_projects(project_service: ProjectService):
    """
    Get all projects.
    """
    projects = project_service.get_all_projects()
    return jsonify([project.to_dict() for project in projects])

@inject
@projects_bp.route('/<project_name>', methods=['GET'])
def get_project(project_name, project_service: ProjectService):
    """
    Get a specific project with the given name by path parameter.
    """
    project = project_service.find_project_by_name(project_name)
    if project:
        return jsonify(project.to_dict())
    return jsonify({"error": "Project not found"}), 404

@inject
@projects_bp.route('/unlisted', methods=['GET'])
def get_unlisted_projects(project_service: ProjectService):
    """
    Get all unlisted projects.
    """
    projects_name_in_filesystem = project_service.get_projects_in_filesystem()
    projects = project_service.get_all_projects()
    projects_name = [project.project_name for project in projects]
    unlisted_projects = []
    for project in projects_name_in_filesystem:
        if project not in projects_name:
            unlisted_projects.append(project)
    return jsonify(unlisted_projects)