import pytest
from unittest.mock import MagicMock, patch
from batteryabn.repositories.cell_repository import CellRepository
from batteryabn.models import Cell

@pytest.fixture
def mock_session():
    # Create a mock session object
    return MagicMock()

@pytest.mark.cell
def test_find_by_name(mock_session):
    # Create a mock Cell instance
    mock_cell = Cell(cell_name="TestCell")
    mock_session.query(Cell).filter_by.return_value.first.return_value = mock_cell

    cell_repository = CellRepository(mock_session)
    result = cell_repository.find_by_name("TestCell")

    assert result == mock_cell
    mock_session.query(Cell).filter_by.assert_called_with(cell_name="TestCell")

@pytest.mark.cell
def test_create_cell(mock_session):
    cell_name = "NewCell"
    cell_repository = CellRepository(mock_session)

    # Check that the create_cell method returns a new Cell instance
    created_cell = cell_repository.create_cell(cell_name)

    assert created_cell.cell_name == cell_name
    mock_session.add.assert_called_once_with(created_cell)
