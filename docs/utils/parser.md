# Parser Module Documentation

This document provides an in-depth overview of the `Parser` class and its methods within the `parser.py` module. The module is designed to parse battery test data files from different instruments and extract relevant test data and metadata. It supports multiple test types including **Arbin**, **BioLogic**, **Neware**, and **Vdf**.

---

## Table of Contents

- [Overview](#overview)
- [Class: Parser](#class-parser)
  - [Attributes](#attributes)
  - [Initialization](#initialization)
- [Parsing Workflow](#parsing-workflow)
- [Method Details](#method-details)
  - [parse(file_path)](#parsefilepath)
  - [parse_arbin(file_path)](#parse_arbinfile_path)
  - [parse_biologic(file_path)](#parse_biologicfile_path)
  - [parse_neware(file_path)](#parse_newarefile_path)
  - [parse_vdf(file_path)](#parse_vdffile_path)
  - [parse_metadata(test_name, test_type)](#parse_metadatatest_name-test_type)
  - [parse_calibration_parameters(file_path)](#parse_calibration_parametersfile_path)
- [Helper Methods](#helper-methods)
- [Usage Example](#usage-example)
- [Error Handling and Logging](#error-handling-and-logging)
- [Future Enhancements](#future-enhancements)

---

## Overview

The `parser.py` module is a key component of the battery testing application. Its main responsibilities include:

- **Reading** and **interpreting** battery test data files.
- **Extracting** raw test data, metadata, and calibration parameters.
- **Supporting** multiple file formats and test types using dedicated parsing functions.

The module leverages external libraries such as **pandas**, **cellpy**, and **BioLogic** to process data files efficiently.

---

## Class: Parser

### Attributes

- **test_name**: Holds the name of the test, derived from the file name.
- **test_type**: Determines the type of test (e.g., Arbin, BioLogic, Neware, Vdf).
- **test_size**: Stores the size of the test data file.
- **raw_test_data**: A pandas DataFrame that stores the parsed test data.
- **raw_metadata**: A dictionary for storing metadata extracted from the test name.
- **calibration_parameters**: Stores calibration parameters loaded from a CSV file.
- **parse_functions**: A dictionary mapping test types to their corresponding parsing functions.

### Initialization

When a new `Parser` object is instantiated (either via `create_parser()` or directly via `Parser()`), it initializes with default values and sets up a mapping of supported test types to their respective parsing functions.

---

## Parsing Workflow

The parsing process is initiated with the **parse(file_path)** method. Here is a high-level overview of the steps involved:

1. **File Validation:** Checks if the provided file path exists.
2. **Clear Previous Data:** Resets attributes to ensure a fresh start.
3. **Extract Test Name:** Uses the file name (sans extension) as the test name.
4. **Determine Test Type:** Infers the test type based on the file extension.
5. **Calculate Test Size:** Retrieves the file size for logging or validation.
6. **Parse Metadata:** Splits the test name to extract metadata using rules defined in constants.
7. **Delegate to Specific Parser:** Calls the appropriate parsing function (e.g., `parse_arbin`, `parse_biologic`) based on the test type.

---

## Method Details

### `parse(file_path: str) -> None`

- **Purpose:** Orchestrates the overall parsing process.
- **Parameters:**
  - `file_path`: The path to the battery test data file.
- **Workflow:**
  1. Validates file existence.
  2. Clears previous data.
  3. Extracts test name, type, and file size.
  4. Parses metadata.
  5. Delegates to the correct parsing function based on test type.

### `parse_arbin(file_path: str) -> None`

- **Purpose:** Parses data from Arbin test data files.
- **Key Steps:**
  - Creates a temporary backup of the file.
  - Uses **cellpy** to read the file and extracts raw, summary, and steps data.
  - Stores raw test data in `self.raw_test_data`.

### `parse_biologic(file_path: str) -> None`

- **Purpose:** Handles the parsing of BioLogic test data files.
- **Key Steps:**
  - Loads the MPR file using the **BioLogic** library.
  - Calculates timestamps and appends them to the data.
  - Stores the resulting DataFrame in `self.raw_test_data`.

### `parse_neware(file_path: str) -> None`

- **Purpose:** Parses test data from Neware files.
- **Key Steps:**
  - Loads the Excel file using **pandas**.
  - Computes timestamps by adjusting the total time.
  - Cleans up unnecessary columns.
  - Stores the processed DataFrame in `self.raw_test_data`.

### `parse_vdf(file_path: str) -> None`

- **Purpose:** Handles the parsing of Vdf formatted test data.
- **Key Steps:**
  - Reads the CSV file and extracts metadata.
  - Stores both raw data and metadata in their respective attributes.

### `parse_metadata(test_name: str, test_type: str) -> None`

- **Purpose:** Extracts metadata from the test name based on the rules defined in constants.
- **Workflow:**
  - Splits the test name using underscores.
  - Zips the resulting values with the expected keys.
  - Updates `self.raw_metadata` with the extracted information.
- **Error Handling:** Raises a `ValueError` if the test name does not conform to expected patterns.

### `parse_calibration_parameters(file_path: str) -> None`

- **Purpose:** Loads calibration parameters from a CSV file.
- **Key Steps:**
  - Reads and iterates through CSV rows.
  - Extracts parameters for each cell.
  - Uses default values when parameters are missing.
  - Updates `self.calibration_parameters` with the parsed information.

---

## Helper Methods

The `Parser` class includes several private helper methods for internal operations:

- **`__get_test_name(file_path: str) -> str`**: Extracts and returns the test name from the file path.
- **`__determine_test_type(file_path: str) -> str`**: Determines the test type based on the file extension.
- **`__get_test_size(file_path: str) -> int`**: Retrieves the file size.
- **`__load_xlsx(file_path: str, sheet: str = 'record') -> pd.DataFrame`**: Loads an Excel file.
- **`__load_vdf_csv(file_path: str) -> pd.DataFrame`**: Reads a Vdf CSV file, handling metadata extraction.
- **`__load_mpr(file_path: str) -> pd.DataFrame`**: Loads an MPR file from BioLogic and extracts start timestamps.
- **`__read_cellpy(file_path: str)`**: Uses **cellpy** to read Arbin data files and returns structured data.

Each of these methods focuses on a specific aspect of the data extraction and processing, keeping the main parsing workflow modular and easier to maintain.

---