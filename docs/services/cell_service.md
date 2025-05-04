# Cell Service Documentation

This document provides instructions and reference information for the `CellService` class. This service handles the creation, processing, and querying of Cell objects along with their associated test records and project information. It integrates with both database repositories and the local filesystem for data persistence and retrieval. For the useage demo, check the code in examples.

## Table of Contents

- [Overview](#overview)
- [Dependencies](#dependencies)
- [Available Methods](#available-methods)
- [Usage Example](#usage-example)

## Overview

The `CellService` class provides an interface for:
- Creating new Cell objects.
- Processing cell data and generating associated images.
- Managing the association between cells and projects.
- Retrieving processed data and test records.
- Loading images and combined cell data from the filesystem.

It leverages dependency injection via `flask_injector` and utilizes various repository and utility classes from the `batteryabn` module.

## Dependencies

The service relies on the following modules and components:
- **Flask Injector**: For dependency injection.
- **batteryabn**: A custom package which includes:
  - **logger** and **Constants** for logging and configuration.
  - **models** defining `Cell` and `Project`.
  - **repositories** that provide:
    - `CellRepository`
    - `TestRecordRepository`
    - `ProjectRepository`
    - `FileSystemRepository`
    - Factory functions: `create_cell_repository`, `create_test_record_repository`, `create_project_repository`, `create_filesystem_repository`
  - **utils** that provide `Processor`, `Viewer`, and general utility functions.

## Available Methods Summary

- **create_cell(cell_name: str)**  
  *Description:* Creates a new Cell (or returns an existing one) using the provided cell name.  
  *Returns:* A `Cell` object.

- **process_cell(cell_name: str, processor: Processor, viewer: Viewer)**  
  *Description:* Processes cell data, generates plots/images, and saves both data and images to the filesystem.

- **process_cells_for_project(project_name: str, processor: Processor, viewer: Viewer)**  
  *Description:* Processes all cells associated with the specified project.

- **generate_cell_images_by_processed_data(cell_name: str, viewer: Viewer)**  
  *Description:* Generates and returns cell images based on pre-processed data.

- **get_processed_data(cell_name: str)**  
  *Description:* Retrieves processed data (cell data, cell cycle metrics, and VDF data) for the given cell.

- **get_data(cell_name: str, data_type: str)**  
  *Description:* Retrieves specific data for the cell from the filesystem.

- **load_cell_images(cell_name: str)**  
  *Description:* Loads cell images directly from the database.

- **get_combined_cell_data(cell_name: str, processor: Processor)**  
  *Description:* Combines cell data with VDF data and saves the combined result.

- **change_cell_project(cell_name: str, new_project_name: str)**  
  *Description:* Changes the project association for the specified cell.

- **get_cycler_vdf_trs(cell: Cell)**  
  *Description:* Retrieves cycler and VDF test records for a cell.

- **find_cell_by_name(cell_name: str)**  
  *Description:* Finds and returns a Cell by its name.

- **find_cells_by_project_name(project_name: str)**  
  *Description:* Returns all Cells associated with a given project.

- **find_cells_by_keyword(keyword: str)**  
  *Description:* Finds all Cells with names matching the provided keyword.

- **delete_cell(cell_name: str)**  
  *Description:* Deletes a Cell and all its associated test records.

- **get_cell_imgs_paths(cell_name: str)**  
  *Description:* Retrieves filesystem paths for the cell's image files.

- **get_cell_htmls_paths(cell_name: str)**  
  *Description:* Retrieves filesystem paths for the cell's HTML image files.

- **get_latest_test_record(cell_name: str)**  
  *Description:* Retrieves the latest non-VDF test record for the cell.

- **get_latest_cell_info(cell_name: str)**  
  *Description:* Retrieves the latest report information for the cell, including test name, timestamp, capacity, protocol, and cycle type.
