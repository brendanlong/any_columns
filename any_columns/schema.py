from collections import defaultdict
from dataclasses import dataclass, field, InitVar
from typing import FrozenSet, Set

from frozendict import frozendict  # type: ignore[attr-defined]

from .column import Column


@dataclass(frozen=True)
class SchemaMatch:
    matches: bool
    matching_columns: frozendict[str, Column]


class AmbigiousColumns(Exception):
    """Raised if more than one Column definition matches the same column in a Schema"""

    def __init__(self, schema: "Schema", column_name: str, column_matches: Set[Column]):
        self.schema = schema
        self.column_name = column_name
        self.column_matches = column_matches


@dataclass(frozen=True)
class Schema:
    """The schema of a spreadsheet, with a set of columns and a name to identify the schema to humans"""

    columns: FrozenSet[Column] = field(init=False)
    columns_init: InitVar[Set[Column]]
    name: str

    def __post_init__(self, columns_init: Set[Column]) -> None:
        # Accept a Set[Column] argument and transparently turn it into a FrozenSet[Column] argument to make this class
        # hashable
        object.__setattr__(self, "columns", frozenset(columns_init))

    def match_columns(self, columns: Set[str]) -> SchemaMatch:
        """
        Check if this schema matches the given set of column names and return the list of matching columns

        Raises AmbigiousColumns if multiple Schema Column definitions match a single column name.
        """
        # This function combines "does this match" and "what is the match" logic for performance reasons, because
        # we don't want to run our set of regexes multiple times

        # Get a mapping from schema columns to column names
        schema_column_to_column_name = {
            schema_column: schema_column.matching_column(columns)
            for schema_column in self.columns
        }

        # Reverse the mapping into a multimap of column names to schema mappings
        column_name_to_schema_columns = defaultdict(set)
        for schema_column, column_name in schema_column_to_column_name.items():
            if column_name is not None:
                column_name_to_schema_columns[column_name].add(schema_column)

        # Find cases where a single column matches multiple column definitions
        for column_name, column_matches in column_name_to_schema_columns.items():
            if len(column_matches) > 1:
                raise AmbigiousColumns(self, column_name, column_matches)

        # Turn the multimap into a normal map now that we've validated that every
        # column name only appears once
        column_name_to_schema_column = {
            column_name: schema_column
            for column_name, [schema_column] in column_name_to_schema_columns.items()
        }

        # The schema matches if every required column found a matching column name
        matches = all(
            not schema_column.required
            or schema_column_to_column_name[schema_column] is not None
            for schema_column in self.columns
        )
        return SchemaMatch(matches, frozendict(column_name_to_schema_column))
