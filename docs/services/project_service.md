# Project Service Documentation

This document provides instructions and reference information for the `ProjectService` class, which handles the creation and querying of Project objects. The service integrates with both a project repository (for database operations) and a filesystem repository (for file system operations). For the useage demo, check the code in examples.

## Table of Contents

- [Overview](#overview)
- [Dependencies](#dependencies)
- [Available Methods](#available-methods)
  - [create_project](#create_project)
  - [find_project_by_name](#find_project_by_name)
  - [get_all_projects](#get_all_projects)
  - [get_projects_in_filesystem](#get_projects_in_filesystem)

## Overview

The `ProjectService` class provides an interface for creating and querying `Project` objects. It leverages dependency injection (using `flask_injector`) to manage its dependencies:
- A project repository to handle database interactions.
- A filesystem repository to manage project files on disk.

This separation of concerns helps maintain a clean and modular codebase.

## Dependencies

The project requires the following dependencies:
- **Flask Injector**: For dependency injection.
- **batteryabn**: A custom module containing:
  - **logger**: For logging events.
  - **models**: Defines the `Project` model.
  - **repositories**: Provides repository classes and factory functions:
    - `ProjectRepository`
    - `FileSystemRepository`
    - `create_project_repository`
    - `create_filesystem_repository`

Make sure these dependencies are properly installed and configured in your environment.

## Available Methods

### create_project(project_name: str) -> Project
- **Description:**  
  Creates a new project instance and adds it to the repository. If a project with the same name already exists, it returns the existing project.
- **Parameters:**  
  - `project_name` (str): The unique name of the project (converted to uppercase).
- **Returns:**  
  - `Project`: The newly created or existing project object.

### find_project_by_name(project_name: str) -> Project
- **Description:**  
  Searches for and returns a project by its name.
- **Parameters:**  
  - `project_name` (str): The name of the project to find.
- **Returns:**  
  - `Project`: The project object matching the given name (or `None` if not found).

### get_all_projects() -> List[Project]
- **Description:**  
  Retrieves all projects from the project repository.
- **Returns:**  
  - `List[Project]`: A list of all project objects stored in the repository.

### get_projects_in_filesystem() -> List[str]
- **Description:**  
  Retrieves all project names available in the filesystem.
- **Returns:**  
  - `List[str]`: A list of project names found in the filesystem.


