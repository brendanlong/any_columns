from typing import Any, Optional, Set
import re

from .column import AmbigiousColumn, ColumnDefinition


class RegexColumn(ColumnDefinition):
    """
    A single column in a spreadsheet identified by a regex

    Note that StringColumn should be preferred where possible because it's much more efficient.
    """

    def __init__(self, pattern: re.Pattern, required: bool = True):
        super().__init__(required)
        self.pattern = pattern

    def _key(self) -> Any:
        return (self.pattern, self.required)

    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other) -> bool:
        if isinstance(other, RegexColumn):
            return self._key() == other._key()
        return NotImplemented

    def matching_column(self, others: Set[str]) -> Optional[str]:
        """
        Finds the column matching this definition in a set of column names if one exists

        Raises `AmbigiousColumn` if more than one column matches
        """
        if isinstance(self.pattern, str):
            if self.pattern in others:
                return self.pattern
            else:
                return None

        matching_columns = {
            column for column in others if self.pattern.fullmatch(column)
        }
        if len(matching_columns) > 1:
            raise AmbigiousColumn(self, matching_columns)

        # Return the one item in the set
        for column in matching_columns:
            return column
        return None
