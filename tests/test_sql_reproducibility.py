"""Unit tests verifying reproducibility and execution of all SQL suite scripts."""

from frogeindrip.config import PROJECT_ROOT


def test_all_sql_files_execute_successfully(db_conn):
    """Verify that every single SQL script in sql/*.sql executes without error on DuckDB."""
    sql_dir = PROJECT_ROOT / "sql"
    sql_files = sorted(list(sql_dir.glob("*.sql")))

    assert len(sql_files) >= 10, f"Expected at least 10 SQL files, found {len(sql_files)}"

    for sql_file in sql_files:
        with open(sql_file) as f:
            query = f.read()

        # Execute query
        try:
            result = db_conn.execute(query).fetchall()
            assert result is not None, f"Query in {sql_file.name} returned None"
        except Exception as e:
            raise AssertionError(f"SQL file {sql_file.name} failed execution: {e}")
