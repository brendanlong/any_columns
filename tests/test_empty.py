from frozendict import frozendict  # type: ignore[attr-defined]

from .context import (
    StringColumn,
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
    assert (
        find_matching_schemas({Schema({StringColumn("a", "column a")}, "test")}, set())
        == set()
    )


def test_sorted_empty_columns() -> None:
    assert (
        find_best_matching_schemas({Schema({StringColumn("a", "column a")}, "test")}, set())
        == []
    )


def test_best_empty_columns() -> None:
    assert (
        find_best_matching_schema({Schema({StringColumn("a", "column a")}, "test")}, set())
        is None
    )


def test_empty_columns_none_required() -> None:
    schema = Schema({StringColumn("a", "column a", required=False)}, "test")
    assert find_matching_schemas({schema}, set()) == {schema}


def test_sorted_empty_columns_none_required() -> None:
    schema = Schema({}, "test")
    assert find_best_matching_schemas({schema}, set()) == [
        SchemaMatch(schema, frozendict({}))
    ]


def test_best_empty_columns_none_required() -> None:
    schema = Schema({StringColumn("a", "column a", required=False)}, "test")
    assert find_best_matching_schema({schema}, set()) == schema


def test_empty_schemas() -> None:
    assert find_matching_schemas(set(), {"a", "column a"}) == set()


def test_sorted_empty_schemas() -> None:
    assert find_best_matching_schemas(set(), {"a", "column a"}) == []


def test_best_empty_schemas() -> None:
    assert find_best_matching_schema(set(), {"a", "column a"}) is None
