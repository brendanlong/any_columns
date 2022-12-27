import pytest

from .context import (
    AmbigiousMatch,
    Column,
    Schema,
    SchemaMatch,
    find_best_matching_schema,
)


def test_two_schemas_with_same_columns() -> None:
    columns = {Column("column a"), Column("column b")}
    schema_a = Schema(columns, "schema a")
    schema_b = Schema(columns, "schema b")
    with pytest.raises(AmbigiousMatch) as exc_info:
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
    assert exc_info.value.matches == {
        SchemaMatch(schema_a, frozenset(columns)),
        SchemaMatch(schema_b, frozenset(columns)),
    }


def test_two_schemas_with_same_columns_different_required() -> None:
    columns_a = {Column("column a", required=False), Column("column b")}
    columns_b = {Column("column a"), Column("column b", required=False)}
    schema_a = Schema(columns_a, "schema a")
    schema_b = Schema(columns_b, "schema b")
    with pytest.raises(AmbigiousMatch) as exc_info:
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
    assert exc_info.value.matches == {
        SchemaMatch(schema_a, frozenset(columns_a)),
        SchemaMatch(schema_b, frozenset(columns_b)),
    }


def test_two_schemas_with_same_columns_one_required() -> None:
    columns_a = {Column("column a"), Column("column b")}
    columns_b = {Column("column a"), Column("column b", required=False)}
    schema_a = Schema(columns_a, "schema a")
    schema_b = Schema(columns_b, "schema b")
    with pytest.raises(AmbigiousMatch) as exc_info:
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
    assert exc_info.value.matches == {
        SchemaMatch(schema_a, frozenset(columns_a)),
        SchemaMatch(schema_b, frozenset(columns_b)),
    }


def test_two_schemas_with_different_number_columns() -> None:
    schema_a = Schema({Column("column a"), Column("column b")}, "schema a")
    schema_b = Schema({Column("column a")}, "schema b")
    # schema a matches more columns so it's better than schema b
    assert (
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
        == schema_a
    )


def test_two_schemas_with_different_columns() -> None:
    schema_a = Schema({Column("column a"), Column("column b")}, "schema a")
    schema_b = Schema({Column("column a"), Column("column c", required=False)}, "schema b")
    # schema a matches more columns so it's better than schema b
    assert (
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
        == schema_a
    )


def test_two_schemas_skip_unmatched() -> None:
    # In this one, schema a has more matching columns, but it's missing a required column so schema b is the best match
    schema_a = Schema({Column("column a"), Column("column b"), Column("column c")}, "schema a")
    schema_b = Schema({Column("column a")}, "schema b")
    assert (
        find_best_matching_schema({schema_a, schema_b}, {"column a", "column b"})
        == schema_b
    )
