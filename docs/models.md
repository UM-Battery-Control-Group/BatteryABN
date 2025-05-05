# BatteryABN Database Models

This document describes the database models used in the BatteryABN application.

## Table of Contents
- [Cell Model](#cell-model)
- [Project Model](#project-model)
- [TestRecord Model](#testrecord-model)
- [Relationships](#relationships)

## Cell Model

The `Cell` model represents a battery cell and stores its related data.

### Table: `cells`

| Column Name | Type | Description |
|-------------|------|-------------|
| `id` | Integer | Primary key |
| `cell_name` | String | Unique cell name (e.g., 'GMJuly2022_CELL002') |
| `project_name` | String | Foreign key to projects.project_name |
| `cell_data` | LargeBinary | Compressed binary data for the cell |
| `cell_cycle_metrics` | LargeBinary | Compressed binary data for cell cycle metrics |
| `cell_data_vdf` | LargeBinary | Compressed binary VDF data |
| `image_cell` | LargeBinary | Binary image data for the cell |
| `image_ccm` | LargeBinary | Binary image data for cell cycle metrics |
| `image_ccm_aht` | LargeBinary | Binary image data for cell cycle metrics AHT |

### Relationships
- `test_records` - One-to-many relationship with `TestRecord` model
- `project` - Many-to-one relationship with `Project` model

### Methods

#### `load_cell_data()`
Loads and decompresses the cell data from the database.

#### `load_cell_cycle_metrics()`
Loads and decompresses the cell cycle metrics from the database.

#### `load_cell_data_vdf()`
Loads and decompresses the cell VDF data from the database.

#### `load_image_cell()`
Converts the binary cell image data to an image.

#### `load_image_ccm()`
Converts the binary cell cycle metrics image data to an image.

#### `load_image_ccm_aht()`
Converts the binary cell cycle metrics AHT image data to an image.

#### `to_dict()`
Converts the Cell object to a dictionary containing basic cell information.

## Project Model

The `Project` model represents a test project that contains a collection of cells.

### Table: `projects`

| Column Name | Type | Description |
|-------------|------|-------------|
| `id` | Integer | Primary key |
| `project_name` | String | Unique project name |
| `qmax` | Float | Maximum charge capacity |
| `i_c20` | Float | C20 current rate |

### Relationships
- `cells` - One-to-many relationship with `Cell` model

### Methods

#### `get_qmax()`
Returns the qmax value or the default value if not set.

#### `get_i_c20()`
Returns the i_c20 value.

#### `to_dict()`
Converts the Project object to a dictionary with project information.

## TestRecord Model

The `TestRecord` model stores battery test data and metadata.

### Table: `testrecords`

| Column Name | Type | Description |
|-------------|------|-------------|
| `id` | Integer | Primary key |
| `test_name` | String | Name of the battery test |
| `test_type` | String | Type of the battery test (e.g., 'Arbin', 'BioLogic', 'Neware', 'Vdf') |
| `cell_name` | String | Foreign key to cells.cell_name |
| `test_data` | LargeBinary | Compressed binary data for test results |
| `test_metadata` | LargeBinary | Compressed binary data for test metadata |
| `start_time` | BIGINT | Unix timestamp for test start time |
| `last_update_time` | BIGINT | Unix timestamp for last update |
| `size` | Integer | Size of the test data in bytes |

### Relationships
- `cell` - Many-to-one relationship with `Cell` model

### Methods

#### `get_test_data()`
Loads and decompresses the test data and returns it as a pandas DataFrame.

#### `get_test_metadata()`
Loads and decompresses the test metadata and returns it as a dictionary.

#### `get_cycle_type()`
Returns the cycle type of the test (e.g., 'CYC', 'RPT', 'Test11', 'EIS', 'CAL', '_F').

#### `is_rpt()`
Checks if the test is an RPT (Reference Performance Test).

#### `is_format()`
Checks if the test is a formation test.

#### `to_dict()`
Converts the TestRecord object to a dictionary with basic test information.

## Relationships

The database models have the following relationships:

1. **Project to Cell**: One-to-many
   - A Project contains multiple Cells
   - Each Cell belongs to one Project

2. **Cell to TestRecord**: One-to-many
   - A Cell has multiple TestRecords
   - Each TestRecord belongs to one Cell

### Entity Relationship Diagram

```
+-------------+       +----------+       +-------------+
|   Project   |1     *|   Cell   |1     *| TestRecord  |
+-------------+       +----------+       +-------------+
| id          |<----->| id       |<----->| id          |
| project_name|       | cell_name|       | test_name   |
| qmax        |       | cell_data|       | test_type   |
| i_c20       |       | ...      |       | test_data   |
+-------------+       +----------+       | ...         |
                                         +-------------+
```