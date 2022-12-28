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
    schema = Schema({StringColumn("a", "column a")}, "test")
    assert find_matching_schemas({schema}, {"a", "column a"}) == {schema}


def test_sorted_one_column_exact() -> None:
    column = StringColumn("a", "column a")
    schema = Schema({StringColumn("a", "column a")}, "test")
    assert find_best_matching_schemas({schema}, {"a", "column a"}) == [
        SchemaMatch(schema, frozendict({"column a": column}))
    ]


def test_best_one_column_exact() -> None:
    column = StringColumn("a", "column a")
    schema = Schema({column}, "test")
    assert find_best_matching_schema({schema}, {"a", "column a"}) == SchemaMatch(
        schema, frozendict({"column a": column})
    )


def test_two_columns_one_required_one_given() -> None:
    schema = Schema(
        {StringColumn("a", "column a"), StringColumn("b", "column b", required=False)},
        "test",
    )
    assert find_matching_schemas(
        {schema},
        {"a", "column a"},
    ) == {schema}


def test_sorted_two_columns_one_required_one_given() -> None:
    column_a = StringColumn("a", "column a")
    schema = Schema({column_a, StringColumn("b", "column b", required=False)}, "test")
    assert find_best_matching_schemas(
        {schema},
        {"a", "column a"},
    ) == [SchemaMatch(schema, frozendict({"column a": column_a}))]


def test_best_two_columns_one_required_one_given() -> None:
    column_a = StringColumn("a", "column a")
    schema = Schema(
        {column_a, StringColumn("b", "column b", required=False)},
        "test",
    )
    assert find_best_matching_schema(
        {schema},
        {"a", "column a"},
    ) == SchemaMatch(schema, frozendict({"column a": column_a}))


def test_two_columns_two_required_one_given() -> None:
    schema = Schema(
        {StringColumn("a", "column a"), StringColumn("b", "column b")}, "test"
    )
    assert (
        find_matching_schemas(
            {schema},
            {"a", "column a"},
        )
        == set()
    )


def test_sorted_two_columns_two_required_one_given() -> None:
    schema = Schema(
        {StringColumn("a", "column a"), StringColumn("b", "column b")}, "test"
    )
    assert (
        find_best_matching_schemas(
            {schema},
            {"a", "column a"},
        )
        == []
    )


def test_best_two_columns_two_required_one_given() -> None:
    schema = Schema(
        {StringColumn("a", "column a"), StringColumn("b", "column b")}, "test"
    )
    assert (
        find_best_matching_schema(
            {schema},
            {"a", "column a"},
        )
        is None
    )


def test_two_columns_two_required_two_given() -> None:
    schema = Schema(
        {StringColumn("a", "column a"), StringColumn("b", "column b")}, "test"
    )
    assert find_matching_schemas(
        {schema},
        {"a", "column a", "b", "column b"},
    ) == {schema}


def test_sorted_two_columns_two_required_two_given() -> None:
    column_a = StringColumn("a", "column a")
    column_b = StringColumn("b", "column b")
    schema = Schema({column_a, column_b}, "test")
    assert find_best_matching_schemas(
        {schema},
        {"a", "column a", "b", "column b"},
    ) == [SchemaMatch(schema, frozendict({"column a": column_a, "column b": column_b}))]


def test_best_two_columns_two_required_two_given() -> None:
    column_a = StringColumn("a", "column a")
    column_b = StringColumn("b", "column b")
    schema = Schema({column_a, column_b}, "test")
    assert find_best_matching_schema(
        {schema},
        {"a", "column a", "b", "column b"},
    ) == SchemaMatch(schema, frozendict({"column a": column_a, "column b": column_b}))
