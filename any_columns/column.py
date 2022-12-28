from abc import ABC, abstractmethod
from typing import Any, Optional, Set


class AmbigiousColumn(Exception):
    """Exception raised if a Column definition matches more than one column header in the input"""

    def __init__(self, column: "Column", matching_columns: Set[str]):
        self.column = column
        self.matching_columns = matching_columns


class Column(ABC):
    """A single column in a spreadsheet"""

    def __init__(self, required: bool = True):
        self.required = required

    @abstractmethod
    def matching_column(self, others: Set[str]) -> Optional[str]:
        """
        Finds the column matching this one in a set of column names if one exists

        Raises `AmbigiousColumn` if more than one column matches
        """
        pass

    @abstractmethod
    def _key(self) -> Any:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
