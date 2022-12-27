from .context import Column, Schema, find_matching_schemas


def test_one_column_exact() -> None:
    schema = Schema({Column("column a")}, "test")
    assert find_matching_schemas({schema}, {"column a"}) == {schema}


def test_two_columns_one_required_one_given() -> None:
    schema = Schema({Column("column a"), Column("column b", required=False)}, "test")
    assert find_matching_schemas(
        {schema},
        {"column a"},
    ) == {schema}


def test_two_columns_two_required_one_given() -> None:
    schema = Schema({Column("column a"), Column("column b")}, "test")
    assert (
        find_matching_schemas(
            {schema},
            {"column a"},
        )
        == set()
    )


def test_two_columns_two_required_two_given() -> None:
    schema = Schema({Column("column a"), Column("column b")}, "test")
    assert find_matching_schemas(
        {schema},
        {"column a", "column b"},
    ) == {schema}
