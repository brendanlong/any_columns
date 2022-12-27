from dataclasses import dataclass, field, InitVar
from typing import FrozenSet, Set

from .column import Column


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

    def matching_columns(self, columns: Set[str]) -> Set[Column]:
        """
        Get the list of columns in this schema that match the given columns

        Note that you will probably also want to run columns_match() to determine if this schema is a match at all.
        """
        return {
            schema_column
            for schema_column in self.columns
            if schema_column.matches_any(columns)
        }

    def columns_match(self, columns: Set[str]) -> bool:
        """
        Check if the columns of this schema match the given columns

        Columns are considered a match if required columns in the schema exist in the given columns.
        """
        return all(
            not schema_column.required or schema_column.matches_any(columns)
            for schema_column in self.columns
        )
