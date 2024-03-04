import pytest
from sqlalchemy.exc import OperationalError
from batteryabn.models.base import engine, DATABASE_URI  

def test_database_uri_loaded():
    """Test that the DATABASE_URI is loaded from the environment."""
    assert DATABASE_URI is not None, "DATABASE_URI is not loaded from environment"

def test_engine_creation():
    """Test that the engine is created successfully."""
    try:
        connection = engine.connect()
    except OperationalError:
        pytest.fail("Failed to create engine. Check the DATABASE_URI in the environment.")
    else:
        connection.close()
