from typing import Any, Optional, Set

from .column import Column


class StringColumn(Column):
    """
    A single column in a spreadsheet identified by an exact string
    """

    def __init__(self, name: str, required: bool = True):
        super().__init__(required)
        self.name = name

    def _key(self) -> Any:
        return (self.name, self.required)

    def __hash__(self) -> int:
        return hash(self._key())

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StringColumn):
            return self._key() == other._key()
        return NotImplemented

    def matching_column(self, others: Set[str]) -> Optional[str]:
        """
        Finds the column matching this one in a set of column names if one exists

        Will never raise `AmbigiousColumn`
        """
        if self.name in others:
            return self.name
        else:
            return None
