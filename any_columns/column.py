from dataclasses import dataclass


@dataclass(frozen=True)
class Column:
    """A single column in a spreadsheet"""

    name: str
    required: bool = True
