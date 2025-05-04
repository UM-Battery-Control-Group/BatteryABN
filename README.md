#  BatteryABN

BatteryABN is a Python module designed for parsing, formatting, and saving battery test data to a database. In addition to data handling, BatteryABN offers methods for processing battery data on a per-cell basis. It currently supports data from Neware and Neware Vdf sources. For more details, check the md files in `docs` folder.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard](#dashboard)
- [Design](#design)
- [License](#license)
- [Questions](#questions)

## Features

- **Data type**
BatteryABN extracts and stores all battery test data directly from the raw test files. It identifies the type of test based on the data file format; for example, a ".mpr" file is considered to represent biological data.

- **Relational database backend**
The BatteryABN package is closely integrated with the specific destination database to which it sends data. It mandates that, for battery data being uploaded to the database, comprehensive metadata must also be provided. Additionally, test records are required to be associated with the corresponding cell.

- **Data Processed**
Data will be processed on a per-cell basis using methods provided by UMBCL. This processing will generate cell cycle metrics, cell data, cell data VDF, and cell data RPT, along with corresponding images. These outputs will then be saved into the database.

## Installation

### Requirements

- Python 3.10 or higher
- The required packages are listed in the `requirements.txt` file

### Installation Instructions

- Install BatteryABN from source code:

```sh
git clone git@github.com:YiLiiu/BatteryABN.git
cd BatteryABN
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
pip install .
```

- Install and Configure PostgreSQL:

Install PostgreSQL from the official website or your system's package manager.
Open the PostgreSQL terminal and create a new database, a new user and grant privileges on the database::

```sh
CREATE DATABASE batteryabn_db;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE batteryabn_db TO myuser;
```

- Use Alembic for Database Migrations

```sh
alembic upgrade head
```

- A .env file in the root directory to store your environment variables:

Add the following line with your PostgreSQL connection string. Replace myuser, mypassword, and batteryabn_db with your PostgreSQL username, password, and database name, respectively.:

```
DATABASE_URI=postgresql://myuser:mypassword@localhost/batteryabn_db
```

- Configure PYTHONPATH:

For the project to run correctly, add its directory to your PYTHONPATH. This step ensures that Python can find the project's modules. Append the following line to your .bashrc, .bash_profile, or .zshrc file, adjusting the path to match your project's location:

```sh
export PYTHONPATH="${PYTHONPATH}:/path/to/BatteryABN"
```

## Usage

- Demo:

The demos for BatteryABN are in the /examples folder. To use BatteryABN, access the test record service as shown in these examples.

```python
app = create_app()

with app.app_context():
    db.create_all()
    parser = Parser()
    formatter = Formatter()
    cell_repository = CellRepository()
    test_record_repository = TestRecordRepository()
    test_record_service = TestRecordService(cell_repository, test_record_repository, project_repository)
    test_record_service.create_and_save_tr(path, parser, formatter)
```

## Dashboard

This dashboard consists of a Flask backend and a React frontend. Follow the steps below to run the application.

### 🚀 Quick Start (Manual)

#### 1. Start the Backend

```bash
cd batteryabn
flask run
```

#### 2. Start the Flask-RQ Worker

```bash
flask rq worker
```
#### 3. Start the Frontend

```bash
cd frontend
npm start
```

### 🐳 Docker (Alternative)
You can also start both frontend and backend using Docker and Docker Compose:

```bash
docker-compose up --build
```

This will automatically build and start all necessary services.

## Design

The BatteryABN project models its domain using two primary classes: TestRecord and Cell. These classes represent the structure and relationships of battery test records and cells within the database. Below, we detail each class and explain their interrelation.

- TestRecord:

The TestRecord class is designed to store detailed information about individual battery tests. Each test record includes several fields:

id: A unique identifier for each test record (primary key).
test_name: The name of the battery test, not unique because the different test type could share same name.
test_type: Specifies the type of battery test (e.g., 'Arbin', 'BioLogic', 'Neware', 'Vdf'), indicating the testing equipment or protocol used.
cell_name: A foreign key linking the test record to its associated battery cell in the cells table.
test_data: Stores the test data as a pickled Python object. This data typically includes time series measurements taken during the test.
test_metadata: Stores metadata about the test (e.g., test conditions, parameters) as a pickled Python dictionary.

- Cell:

The Cell class represents a battery cell and contains two main attributes(Will add more in the future):

id: A unique identifier for each cell (primary key).
cell_name: The name of the cell, which is unique across the database.

- Relationship between TestRecord and Cell:

The relationship between TestRecord and Cell is fundamental to the BatteryABN database schema. It is defined as a one-to-many relationship:

One-to-Many: A single Cell can be associated with multiple TestRecord instances, but each TestRecord is linked to exactly one Cell. This reflects the real-world scenario where a battery cell undergoes multiple tests over time, generating multiple test records.
This relationship is implemented using a foreign key (cell_name in TestRecord pointing to cell_name in Cell) and SQLAlchemy's relationship function. The relationship allows for easy navigation between linked instances of these classes, enabling efficient queries and data manipulation within the application.

## License

This project is licensed under the MIT License.

## Questions

If you have any questions or encounter any bugs, please raise an issue in our repository or send an email to ziyiliu@umich.edu. We greatly appreciate your feedback.