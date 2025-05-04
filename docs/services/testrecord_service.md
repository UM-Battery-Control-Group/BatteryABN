# TestRecordService — Battery Test Record Management

This module provides the `TestRecordService` class and a factory function `create_test_record_service` to handle the creation, retrieval, and deletion of battery test records. It integrates with the database models `TestRecord`, `Cell`, and `Project`, and relies on parsing and formatting utilities. Core method for this service is `create_and_save_tr`.

---

## Factory Function

### `create_test_record_service(session=None)`
Initializes and returns a `TestRecordService` instance using repository factories.

**Parameters:**
- `session` *(optional)*: SQLAlchemy session object. If not provided, a default session will be used.

**Returns:**  
- `TestRecordService` instance

---

## Class: `TestRecordService`

Handles saving and retrieving battery test data, and ensures the associated cell and project entries are properly linked and maintained.
## Dependencies
- `batteryabn.models`: `TestRecord`, `Cell`, `Project`
- `batteryabn.repositories`: `CellRepository`, `TestRecordRepository`, `ProjectRepository`
- `batteryabn.utils`: `Parser`, `Formatter`, `Utils`
- `flask_injector`: for dependency injection


---

### `create_and_save_tr(path, parser, formatter, reset=False)`
Parses a single test data file and creates or updates the corresponding `TestRecord`.
**Parameters:**
- `path` *(str)*: Path to the test data file.
- `parser` *(Parser)*: Parses the file into structured data.
- `formatter` *(Formatter)*: Formats parsed data for storage.
- `reset` *(bool)*: If `True`, overrides existing records. *(default: False)*


### `create_and_save_trs(path, key_word, parser, formatter, file_extensions=[...], reset=False)`
Processes multiple test data files within a directory using keyword and extension filters.
**Parameters:**
- `path` *(str)*: Directory path to search.
- `key_word` *(str)*: Keyword filter for filenames.
- `parser` *(Parser)*: Parser instance.
- `formatter` *(Formatter)*: Formatter instance.
- `file_extensions` *(list[str])*: File types to search. *(default: [.xlsx, .csv, .mpr])*
- `reset` *(bool)*: Whether to override existing records.


### `find_test_record_by_name(test_name, test_type)`
Finds a single test record by name and type.
**Parameters:**
- `test_name` *(str)*  
- `test_type` *(str)*
**Returns:**  
- `TestRecord` instance or `None`


### `find_test_records_by_cell_name(cell_name)`
Fetches all test records linked to a specific battery cell.
**Parameters:**
- `cell_name` *(str)*
**Returns:**  
- `List[TestRecord]`


### `find_test_records_by_keyword(keyword)`
Searches for test records using a metadata keyword.
**Parameters:**
- `keyword` *(str)*
**Returns:**  
- `List[TestRecord]`


### `delete_test_record(test_name, test_type)`
Deletes a test record from the database.
**Parameters:**
- `test_name` *(str)*  
- `test_type` *(str)*


### `delete_test_records_by_cell_name(cell_name)`
Deletes all test records associated with a specific cell.
**Parameters:**
- `cell_name` *(str)*
