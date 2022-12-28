from typing import Any, Optional, Set

from .column import ColumnDefinition


class StringColumn(ColumnDefinition):
    """
    A single column in a spreadsheet identified by an exact string
    """

    def __init__(self, name: str, pattern: str, required: bool = True):
        super().__init__(name, required)
        self.name = name
        self.pattern = pattern

    def _key(self) -> Any:
        return (self.name, self.pattern, self.required)

    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StringColumn):
            return self._key() == other._key()
        return NotImplemented

    def matching_column(self, others: Set[str]) -> Optional[str]:
        """
        Finds the column matching this definition in a set of column names if one exists

        Will never raise `AmbigiousColumn`
        """
        if self.pattern in others:
            return self.pattern
        else:
            return None
