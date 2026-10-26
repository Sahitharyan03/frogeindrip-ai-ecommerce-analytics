"""Pytest configuration and shared fixtures for Frogeindrip test suite."""

import sys
from pathlib import Path

import duckdb
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from frogeindrip.config import DEFAULT_RANDOM_SEED
from frogeindrip.data.generator import generate_synthetic_data
from frogeindrip.etl.pipeline import FrogeindripETL


@pytest.fixture(scope="session")
def synthetic_data_dfs():
    """Generate fresh deterministic synthetic datasets for testing."""
    return generate_synthetic_data(seed=DEFAULT_RANDOM_SEED, num_customers=100, save_csv=False)


@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    """Create a temporary DuckDB database for isolated testing."""
    temp_dir = tmp_path_factory.mktemp("db_test")
    test_db = temp_dir / "test_frogeindrip.duckdb"
    etl = FrogeindripETL(db_path=test_db, seed=DEFAULT_RANDOM_SEED)
    etl.run()
    etl.close()
    return test_db


@pytest.fixture
def db_conn(test_db_path):
    """Provide a read-only connection to the test DuckDB instance."""
    conn = duckdb.connect(str(test_db_path), read_only=True)
    yield conn
    conn.close()
