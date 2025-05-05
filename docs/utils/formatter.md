# Formatter Module Documentation

This document provides an in-depth overview of the `Formatter` class and its methods within the `formatter.py` module. The module is designed to format raw battery test data and metadata into a structured and consistent format for further analysis and visualization. It supports multiple test types including **Arbin**, **BioLogic**, **Neware**, and **Vdf**.

---

## Table of Contents

- [Overview](#overview)
- [Class: Formatter](#class-formatter)
  - [Attributes](#attributes)
  - [Initialization](#initialization)
- [Formatting Workflow](#formatting-workflow)
- [Method Details](#method-details)
  - [format_data(data, metadata, test_type)](#format_datadata-metadata-test_type)
  - [format_test_data(data, test_type)](#format_test_data-data-test_type)
  - [format_metadata(metadata)](#format_metadatametadata)
  - [format_calibration_parameters(calibration_parameters)](#format_calibration_parameterscalibration_parameters)
  - [add_calibration_parameters(df)](#add_calibration_parametersdf)
  - [clear()](#clear)
- [Usage Example](#usage-example)
- [Logging and Future Enhancements](#logging-and-future-enhancements)

---

## Overview

The `formatter.py` module is a core component responsible for transforming raw battery test data and metadata into a well-structured and formatted DataFrame. It performs tasks such as:

- Dropping unnecessary columns and empty rows.
- Renaming columns according to the test type.
- Calculating additional parameters (e.g., AHT through integration of current data).
- Converting and formatting timestamps.
- Incorporating calibration parameters when available.

This process is essential for ensuring that the data is ready for analysis and further processing.

---

## Class: Formatter

### Attributes

- **timezone**: Timezone used for formatting; defaults to the value defined in constants if not provided.
- **test_data**: A pandas DataFrame that stores the formatted test data.
- **metadata**: A dictionary for storing formatted metadata.
- **cell_name**: The identifier for the test data, derived from the metadata.
- **start_time**: The start timestamp extracted from the test data.
- **last_update_time**: The timestamp of the most recent update in the test data.
- **calibration_parameters**: A dictionary containing calibration parameters for cells.

### Initialization

When a new `Formatter` object is instantiated via `create_formatter(timezone)` or directly using `Formatter(timezone)`, it sets the timezone (defaulting to a constant value if none is provided) and initializes the attributes to store test data and metadata.

---

## Formatting Workflow

The formatting process involves the following steps:

1. **Clear Previous Data:** Reset formatted data and metadata.
2. **Format Metadata:** Standardize and store metadata, including deriving the cell name.
3. **Format Test Data:** Process the raw test data by:
   - Dropping unnamed and empty columns.
   - Renaming columns according to test type.
   - Adding additional columns (e.g., temperature, step index, and AHT).
   - Calculating AHT by integrating the current over time.
   - Adjusting data (e.g., temperature cleaning and converting time strings to seconds) based on the test type.
4. **Incorporate Calibration Parameters:** For VDF test data, calibration parameters are added to the DataFrame.

---

## Method Details

### `format_data(data: pd.DataFrame, metadata: dict, test_type: str) -> pd.DataFrame`

- **Purpose:**  
  Orchestrates the formatting process by clearing previous data, formatting metadata, and then formatting test data based on the test type.
- **Parameters:**
  - `data`: The raw battery test data as a pandas DataFrame.
  - `metadata`: Raw metadata associated with the test data.
  - `test_type`: A string representing the test type (e.g., "Arbin", "BioLogic", "Neware", "Vdf").
- **Returns:**  
  A formatted pandas DataFrame containing the test data.

### `format_test_data(data: pd.DataFrame, test_type: str) -> None`

- **Purpose:**  
  Processes and formats the raw test data.  
- **Key Steps:**
  - Creates a copy of the data and removes unnamed columns and empty rows.
  - Formats the columns and renames them using a dictionary specific to the test type.
  - Adds additional columns such as temperature, step index, and AHT (calculated via integration of current).
  - Handles specific test type adjustments (e.g., scaling current for BioLogic and adjusting temperature/time values for Neware).
  - Validates that the lengths of key columns are consistent.
  - Extracts start and last update timestamps from the data.
- **Notes:**  
  Uses helper functions from the `Utils` module for common operations.

### `format_metadata(metadata: dict) -> None`

- **Purpose:**  
  Formats and standardizes the raw metadata.
- **Key Steps:**
  - Uses `Utils.format_dict` to clean and structure the metadata.
  - Derives the cell name by combining the "Project Name" and "Cell ID" fields.
  - Stores the formatted metadata in the class attribute.

### `format_calibration_parameters(calibration_parameters: dict) -> None`

- **Purpose:**  
  Accepts and stores calibration parameters for later use in data formatting.
- **Notes:**  
  Although commented-out logic exists for a more refined parameter formatting, the current implementation directly assigns the provided parameters.

### `add_calibration_parameters(df: pd.DataFrame) -> pd.DataFrame`

- **Purpose:**  
  Incorporates calibration parameters into the test data DataFrame.
- **Key Steps:**
  - Adds columns for calibration parameters (X1, X2, and C) with default constant values.
  - If calibration parameters exist for the given cell, updates the DataFrame with these values based on specific conditions related to the test type.
- **Returns:**  
  The modified DataFrame with calibration parameter columns added.

### `clear() -> None`

- **Purpose:**  
  Resets the formatted test data and metadata to their default states.

---