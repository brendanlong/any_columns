from frozendict import frozendict  # type: ignore[attr-defined]

from .context import (
    StringColumn,
    Schema,
    SchemaMatch,
    find_best_matching_schema,
    find_best_matching_schemas,
    find_matching_schemas,
)


def test_one_column_exact() -> None:
    schema = Schema({StringColumn("column a")}, "test")
    assert find_matching_schemas({schema}, {"column a"}) == {schema}


def test_sorted_one_column_exact() -> None:
    column = StringColumn("column a")
    schema = Schema({StringColumn("column a")}, "test")
    assert find_best_matching_schemas({schema}, {"column a"}) == [
        SchemaMatch(schema, frozendict({"column a": column}))
    ]


def test_best_one_column_exact() -> None:
    schema = Schema({StringColumn("column a")}, "test")
    assert find_best_matching_schema({schema}, {"column a"}) == schema


def test_two_columns_one_required_one_given() -> None:
    schema = Schema(
        {StringColumn("column a"), StringColumn("column b", required=False)}, "test"
    )
    assert find_matching_schemas(
        {schema},
        {"column a"},
    ) == {schema}


def test_sorted_two_columns_one_required_one_given() -> None:
    column_a = StringColumn("column a")
    schema = Schema({column_a, StringColumn("column b", required=False)}, "test")
    assert find_best_matching_schemas(
        {schema},
        {"column a"},
    ) == [SchemaMatch(schema, frozendict({"column a": column_a}))]


def test_best_two_columns_one_required_one_given() -> None:
    schema = Schema(
        {StringColumn("column a"), StringColumn("column b", required=False)}, "test"
    )
    assert (
        find_best_matching_schema(
            {schema},
            {"column a"},
        )
        == schema
    )


def test_two_columns_two_required_one_given() -> None:
    schema = Schema({StringColumn("column a"), StringColumn("column b")}, "test")
    assert (
        find_matching_schemas(
            {schema},
            {"column a"},
        )
        == set()
    )


def test_sorted_two_columns_two_required_one_given() -> None:
    schema = Schema({StringColumn("column a"), StringColumn("column b")}, "test")
    assert (
        find_best_matching_schemas(
            {schema},
            {"column a"},
        )
        == []
    )


def test_best_two_columns_two_required_one_given() -> None:
    schema = Schema({StringColumn("column a"), StringColumn("column b")}, "test")
    assert (
        find_best_matching_schema(
            {schema},
            {"column a"},
        )
        is None
    )


def test_two_columns_two_required_two_given() -> None:
    schema = Schema({StringColumn("column a"), StringColumn("column b")}, "test")
    assert find_matching_schemas(
        {schema},
        {"column a", "column b"},
    ) == {schema}


def test_sorted_two_columns_two_required_two_given() -> None:
    column_a = StringColumn("column a")
    column_b = StringColumn("column b")
    schema = Schema({column_a, column_b}, "test")
    assert find_best_matching_schemas(
        {schema},
        {"column a", "column b"},
    ) == [SchemaMatch(schema, frozendict({"column a": column_a, "column b": column_b}))]


def test_best_two_columns_two_required_two_given() -> None:
    schema = Schema({StringColumn("column a"), StringColumn("column b")}, "test")
    assert (
        find_best_matching_schema(
            {schema},
            {"column a", "column b"},
        )
        == schema
    )
