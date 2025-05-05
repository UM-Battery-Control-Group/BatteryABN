# BatteryABN API Documentation

This document provides details on all the available endpoints in the BatteryABN API.

## Table of Contents
- [Cells API](#cells-api)
- [Test Records API](#test-records-api)
- [Tasks API](#tasks-api)
- [Projects API](#projects-api)

## Cells API

The Cells API provides endpoints for retrieving information about battery cells.

### Get Cells by Project

Retrieves all cells associated with a specific project.

```
GET /cells/project/{project_name}
```

**Parameters:**
- `project_name` (path parameter): The name of the project

**Responses:**
- `200 OK`: Returns an array of cell objects
- `404 Not Found`: If the project does not exist or has no cells

### Get Cell by Name

Retrieves a specific cell by its name.

```
GET /cells/{cell_name}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns the cell object
- `404 Not Found`: If the cell does not exist

### Get Cell Images

Retrieves images for a specific cell.

```
GET /cells/{cell_name}/images/{number}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell
- `number` (path parameter): The index of the image to retrieve

**Responses:**
- `200 OK`: Returns the image file with MIME type 'image/png'
- `404 Not Found`: If the image does not exist

### Get Cell HTML Files

Retrieves HTML files for a specific cell.

```
GET /cells/{cell_name}/htmls/{number}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell
- `number` (path parameter): The index of the HTML file to retrieve

**Responses:**
- `200 OK`: Returns the HTML file with MIME type 'text/html'
- `404 Not Found`: If the HTML file does not exist

### Search Cells

Searches for cells by keyword.

```
GET /cells/search/{keyword}
```

**Parameters:**
- `keyword` (path parameter): The keyword to search for

**Responses:**
- `200 OK`: Returns an array of cell objects that match the keyword
- `404 Not Found`: If no cells match the keyword

### Get Latest Test Record for Cell

Retrieves the latest test record for a specific cell.

```
GET /cells/{cell_name}/trs/latest
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns the latest test record object
- `404 Not Found`: If no test record exists for the cell

### Get Latest Cell Information

Retrieves the latest information for a specific cell.

```
GET /cells/{cell_name}/info/latest
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns the latest cell information
- `404 Not Found`: If no information exists for the cell

## Test Records API

The Test Records API provides endpoints for retrieving test record data.

### Get Test Records by Cell Name

Retrieves all test records for a specific cell.

```
GET /tests/cell/{cell_name}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns an array of test record objects
- `404 Not Found`: If the cell does not exist or has no test records

### Get Test Record by Name

Retrieves a specific test record by its name.

```
GET /tests/{tr_name}
```

**Parameters:**
- `tr_name` (path parameter): The name of the test record
- `test_type` (query parameter): The type of the test

**Responses:**
- `200 OK`: Returns the test record object
- `404 Not Found`: If the test record does not exist

### Search Test Records

Searches for test records by keyword.

```
GET /tests/search/{keyword}
```

**Parameters:**
- `keyword` (path parameter): The keyword to search for

**Responses:**
- `200 OK`: Returns an array of test record objects that match the keyword
- `404 Not Found`: If no test records match the keyword

### Get Test Record Metadata

Retrieves the metadata for a specific test record.

```
GET /tests/{tr_name}/metadata
```

**Parameters:**
- `tr_name` (path parameter): The name of the test record
- `test_type` (query parameter): The type of the test

**Responses:**
- `200 OK`: Returns the metadata object
- `404 Not Found`: If the test record does not exist

### Get Test Record Data

Retrieves the data for a specific test record.

```
GET /tests/{tr_name}/data
```

**Parameters:**
- `tr_name` (path parameter): The name of the test record
- `test_type` (query parameter): The type of the test

**Responses:**
- `200 OK`: Returns the test data as JSON array
- `404 Not Found`: If the test record does not exist

## Tasks API

The Tasks API provides endpoints for managing background tasks such as updating test records and processing cells.

### Update Test Records

Updates test records for a specific cell.

```
POST /tasks/trs/update/{cell_name}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns a message indicating the task has been enqueued
- `404 Not Found`: If the cell does not exist or the data directory is not found

### Reset Test Records

Resets and updates test records for a specific cell.

```
POST /tasks/trs/reset/{cell_name}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns a message indicating the task has been enqueued
- `404 Not Found`: If the cell does not exist or the data directory is not found

### Create Cell

Creates a cell and processes its test records.

```
POST /tasks/cell/create/{cell_name}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns a message indicating the task has been enqueued
- `404 Not Found`: If the cell data directory does not exist

### Update Project

Updates all cells for a specific project.

```
POST /tasks/project/update/{project_name}
```

**Parameters:**
- `project_name` (path parameter): The name of the project

**Responses:**
- `200 OK`: Returns a message indicating the task has been enqueued
- `404 Not Found`: If the project data directory does not exist

### Process Cell

Processes a specific cell.

```
POST /tasks/cell/process/{cell_name}
```

**Parameters:**
- `cell_name` (path parameter): The name of the cell

**Responses:**
- `200 OK`: Returns a message indicating the task has been enqueued
- `404 Not Found`: If the cell does not exist

### Get Tasks Status

Retrieves the status of all tasks.

```
GET /tasks/status
```

**Responses:**
- `200 OK`: Returns the status of all tasks

### Clear All Tasks

Clears all tasks from the queue.

```
POST /tasks/clear
```

**Responses:**
- `200 OK`: Returns a message indicating all tasks have been cleared

### Clear Finished Tasks

Clears all finished tasks from the queue.

```
POST /tasks/clear/finished
```

**Responses:**
- `200 OK`: Returns information about cleared tasks

### Clear Failed Tasks

Clears all failed tasks from the queue.

```
POST /tasks/clear/failed
```

**Responses:**
- `200 OK`: Returns information about cleared tasks

## Projects API

The Projects API provides endpoints for retrieving project information.

### Get All Projects

Retrieves all projects.

```
GET /projects/
```

**Responses:**
- `200 OK`: Returns an array of project objects

### Get Project by Name

Retrieves a specific project by its name.

```
GET /projects/{project_name}
```

**Parameters:**
- `project_name` (path parameter): The name of the project

**Responses:**
- `200 OK`: Returns the project object
- `404 Not Found`: If the project does not exist

### Get Unlisted Projects

Retrieves all projects that exist in the filesystem but are not registered in the database.

```
GET /projects/unlisted
```

**Responses:**
- `200 OK`: Returns an array of project names