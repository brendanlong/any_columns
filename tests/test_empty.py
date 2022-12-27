from .context import (
    Column,
    Schema,
    SchemaMatch,
    find_best_matching_schema,
    find_best_matching_schemas,
    find_matching_schemas,
)


def test_empty_schemas_and_columns() -> None:
    assert find_matching_schemas(set(), set()) == set()


def test_sorted_empty_schemas_and_columns() -> None:
    assert find_best_matching_schemas(set(), set()) == []


def test_best_empty_schemas_and_columns() -> None:
    assert find_best_matching_schema(set(), set()) is None


def test_empty_columns() -> None:
    assert find_matching_schemas({Schema({Column("column a")}, "test")}, set()) == set()


def test_sorted_empty_columns() -> None:
    assert (
        find_best_matching_schemas({Schema({Column("column a")}, "test")}, set()) == []
    )


def test_best_empty_columns() -> None:
    assert (
        find_best_matching_schema({Schema({Column("column a")}, "test")}, set()) is None
    )


def test_empty_columns_none_required() -> None:
    schema = Schema({Column("column a", required=False)}, "test")
    assert find_matching_schemas({schema}, set()) == {schema}


def test_sorted_empty_columns_none_required() -> None:
    schema = Schema({}, "test")
    assert find_best_matching_schemas({schema}, set()) == [SchemaMatch(schema, set())]


def test_best_empty_columns_none_required() -> None:
    schema = Schema({Column("column a", required=False)}, "test")
    assert find_best_matching_schema({schema}, set()) == schema


def test_empty_schemas() -> None:
    assert find_matching_schemas(set(), {"column a"}) == set()


def test_sorted_empty_schemas() -> None:
    assert find_best_matching_schemas(set(), {"column a"}) == []


def test_best_empty_schemas() -> None:
    assert find_best_matching_schema(set(), {"column a"}) is None
