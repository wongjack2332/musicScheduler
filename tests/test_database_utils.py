from src import database_utils


def test_database_connection():
    connection = database_utils.get_connection()
    assert connection is not None