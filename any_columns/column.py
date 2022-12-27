from dataclasses import dataclass
from typing import Set


@dataclass(frozen=True)
class Column:
    """A single column in a spreadsheet"""

    name: str
    required: bool = True

    def matches_any(self, others: Set[str]) -> bool:
        """Determine if this column matches any of the input columns"""
        return self.name in others
