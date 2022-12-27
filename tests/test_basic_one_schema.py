from .context import (
    Column,
    Schema,
    SchemaMatch,
    find_best_matching_schema,
    find_best_matching_schemas,
    find_matching_schemas,
)


def test_one_column_exact() -> None:
    schema = Schema({Column("column a")}, "test")
    assert find_matching_schemas({schema}, {"column a"}) == {schema}


def test_sorted_one_column_exact() -> None:
    column = Column("column a")
    schema = Schema({Column("column a")}, "test")
    assert find_best_matching_schemas({schema}, {"column a"}) == [
        SchemaMatch(schema, {column})
    ]


def test_best_one_column_exact() -> None:
    schema = Schema({Column("column a")}, "test")
    assert find_best_matching_schema({schema}, {"column a"}) == schema


def test_two_columns_one_required_one_given() -> None:
    schema = Schema({Column("column a"), Column("column b", required=False)}, "test")
    assert find_matching_schemas(
        {schema},
        {"column a"},
    ) == {schema}


def test_sorted_two_columns_one_required_one_given() -> None:
    column_a = Column("column a")
    schema = Schema({column_a, Column("column b", required=False)}, "test")
    assert find_best_matching_schemas(
        {schema},
        {"column a"},
    ) == [SchemaMatch(schema, {column_a})]


def test_best_two_columns_one_required_one_given() -> None:
    schema = Schema({Column("column a"), Column("column b", required=False)}, "test")
    assert (
        find_best_matching_schema(
            {schema},
            {"column a"},
        )
        == schema
    )


def test_two_columns_two_required_one_given() -> None:
    schema = Schema({Column("column a"), Column("column b")}, "test")
    assert (
        find_matching_schemas(
            {schema},
            {"column a"},
        )
        == set()
    )


def test_sorted_two_columns_two_required_one_given() -> None:
    schema = Schema({Column("column a"), Column("column b")}, "test")
    assert (
        find_best_matching_schemas(
            {schema},
            {"column a"},
        )
        == []
    )


def test_best_two_columns_two_required_one_given() -> None:
    schema = Schema({Column("column a"), Column("column b")}, "test")
    assert (
        find_best_matching_schema(
            {schema},
            {"column a"},
        )
        is None
    )


def test_two_columns_two_required_two_given() -> None:
    schema = Schema({Column("column a"), Column("column b")}, "test")
    assert find_matching_schemas(
        {schema},
        {"column a", "column b"},
    ) == {schema}


def test_sorted_two_columns_two_required_two_given() -> None:
    columns = {Column("column a"), Column("column b")}
    schema = Schema(columns, "test")
    assert find_best_matching_schemas(
        {schema},
        {"column a", "column b"},
    ) == [SchemaMatch(schema, columns)]


def test_best_two_columns_two_required_two_given() -> None:
    schema = Schema({Column("column a"), Column("column b")}, "test")
    assert (
        find_best_matching_schema(
            {schema},
            {"column a", "column b"},
        )
        == schema
    )
