from .context import Column, Schema, find_matching_schemas


def test_empty_schemas_and_columns() -> None:
    assert find_matching_schemas(set(), set()) == set()


def test_empty_columns() -> None:
    assert find_matching_schemas({Schema({Column("column a")}, "test")}, set()) == set()


def test_empty_columns_none_required() -> None:
    schema = Schema({Column("column a", required=False)}, "test")
    assert find_matching_schemas({schema}, set()) == {schema}


def test_empty_schemas() -> None:
    assert find_matching_schemas(set(), {"column a"}) == set()
