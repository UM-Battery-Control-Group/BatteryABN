### Repo Structure

Currently, processed data is stored in the local file system. The system is designed to support future migration to database storage if needed.

```shell

├── alembic            # Handles database migrations and version control
├── examples           # Contains example scripts demonstrating system usage
├── tests              # Unit, integration, and data tests for ensuring code quality and functionality
│   ├── data           # Test data used for various test cases
│   ├── integration    # Integration tests for different components
│   ├── units          # Unit tests for individual functions or classes
├── batteryabn         # Core of the application
│   ├── apis           # API layer exposing endpoints for interacting with services
│   ├── models         # Data models representing core entities such as Cell, Project, and TestRecord
│   │    ├── cell.py       # Model for the Cell entity, including attributes and methods
│   │    ├── project.py    # Model for the Project entity, containing project details
│   │    ├── testrecord.py # Model for TestRecord, representing test data associated with cells
│   ├── repositories   # Data access layer interacting with the database and local files
│   ├── services       # Business logic layer, orchestrating operations and interactions across 
repositories
│   ├── utils          # Utility modules for data parsing, formatting, processing, and visualization
│   │    ├── parser       # Parsing raw data from various file formats
│   │    ├── formatter    # Formatting parsed data into a structured form
│   │    ├── processor    # Processing the structured data for analysis and usage
│   │    ├── viewer       # Generating visual representations (plots, images) of processed data

```


1. Project Overview

The project involves designing and implementing a system for managing battery test data using the Model-Repository-Service (MRS) architecture. The system facilitates the storage, processing, and retrieval of battery cell data, test records, and associated project information. It integrates with a local filesystem for storing large datasets and generated images.

2. Key Components

Models: The primary models are Cell, TestRecord, and Project.
Cell: Stores data related to a specific battery cell. Each cell is uniquely identified by a cell_name and belongs to a Project.
TestRecord: Contains data from battery tests. Each test record is associated with a Cell.
Project: Represents a project under which multiple battery cells are tested.
Relationships:
A Cell has many TestRecords.
A Cell belongs to a Project, and each Project can have multiple Cells.

3. Architecture

The system follows the MRS architecture:

Model Layer: Defines the structure of the database entities (Cell, TestRecord, Project) and their relationships using SQLAlchemy ORM. If you want to modify the data structure in the database, change this part.

Repository Layer: This layer handles all interactions with the database and local files. It provides methods to query, add, and delete records, ensuring that all data is properly saved and updated. However, users should not interact with this layer directly. Instead, it exposes an API to the service layer, allowing the service layer to manage and control all database operations and business logic.

Service Layer: Implements business logic for interacting with the repository layer, such as creating new cells, processing test data, and managing files.

4. Service Layer Details

CellService:
Manages cell creation, processing, and data storage.
Retrieves processed data and images, facilitates saving to local files, and changes cell-project associations.
Uses a Processor and Viewer for data processing and image generation, storing the results locally via FileSystemRepository.
TestRecordService:
Handles creation, saving, and deletion of TestRecord objects.
Parses test data using a Parser, formats it with a Formatter, and saves it along with the associated cell and project metadata.

5. Filesystem Integration

The system uses a local file storage solution via the FileSystemRepository. Processed data, cell cycle metrics, and images are saved as:

CSV and PKL (Pickle): For structured data.
PNG: For visualization (graphs and images).

6. Key Functionalities

Cell Management: Create, retrieve, update, or delete battery cells. Assign cells to projects.
Test Data Processing: Parse test data files, process them using external processors, and store the results both locally and in the repository.
Image Generation: Generate plots (e.g., cell cycle metrics) using a Viewer and save the images for future retrieval.
File Handling: Load and save data in compressed formats (e.g., PKL.gz) and images in PNG.
