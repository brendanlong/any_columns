from frozendict import frozendict  # type: ignore[attr-defined]


import pytest

from .context import (
    AmbigiousMatch,
    ColumnDefinition,
    StringColumn,
    Schema,
    SchemaMatch,
    find_best_matching_schema,
)


def test_two_schemas_with_same_columns() -> None:
    column_a = StringColumn("column a")
    column_b = StringColumn("column b")
    schema_a = Schema({column_a, column_b}, "schema a")
    schema_b = Schema({column_a, column_b}, "schema b")
    with pytest.raises(AmbigiousMatch) as exc_info:
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
    assert exc_info.value.matches == {
        SchemaMatch(schema_a, frozendict({"column a": column_a, "column b": column_b})),
        SchemaMatch(schema_b, frozendict({"column a": column_a, "column b": column_b})),
    }


def test_two_schemas_with_same_columns_different_required() -> None:
    column_a_required = StringColumn("column a")
    column_a_optional = StringColumn("column a", required=False)
    column_b_required = StringColumn("column b")
    column_b_optional = StringColumn("column b", required=False)
    schema_a = Schema({column_a_optional, column_b_required}, "schema a")
    schema_b = Schema({column_a_required, column_b_optional}, "schema b")
    with pytest.raises(AmbigiousMatch) as exc_info:
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
    assert exc_info.value.matches == {
        SchemaMatch(
            schema_a,
            frozendict({"column a": column_a_optional, "column b": column_b_required}),
        ),
        SchemaMatch(
            schema_b,
            frozendict({"column a": column_a_required, "column b": column_b_optional}),
        ),
    }


def test_two_schemas_with_same_columns_one_required() -> None:
    column_a = StringColumn("column a")
    column_b_required = StringColumn("column b")
    column_b_optional = StringColumn("column b", required=False)
    schema_a = Schema({column_a, column_b_required}, "schema a")
    schema_b = Schema({column_a, column_b_optional}, "schema b")
    with pytest.raises(AmbigiousMatch) as exc_info:
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
    assert exc_info.value.matches == {
        SchemaMatch(
            schema_a,
            frozendict({"column a": column_a, "column b": column_b_required}),
        ),
        SchemaMatch(
            schema_b,
            frozendict({"column a": column_a, "column b": column_b_optional}),
        ),
    }


def test_two_schemas_with_different_number_columns() -> None:
    schema_a = Schema({StringColumn("column a"), StringColumn("column b")}, "schema a")
    schema_b = Schema({StringColumn("column a")}, "schema b")
    # schema a matches more columns so it's better than schema b
    assert (
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
        == schema_a
    )


def test_two_schemas_with_different_columns() -> None:
    schema_a = Schema({StringColumn("column a"), StringColumn("column b")}, "schema a")
    schema_b = Schema(
        {StringColumn("column a"), StringColumn("column c", required=False)}, "schema b"
    )
    # schema a matches more columns so it's better than schema b
    assert (
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
        == schema_a
    )


def test_two_schemas_skip_unmatched() -> None:
    # In this one, schema a has more matching columns, but it's missing a required column so schema b is the best match
    schema_a = Schema(
        {StringColumn("column a"), StringColumn("column b"), StringColumn("column c")},
        "schema a",
    )
    schema_b = Schema({StringColumn("column a")}, "schema b")
    assert (
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
        == schema_b
    )
