from dataclasses import dataclass
from typing import List, Optional, Set

from frozendict import frozendict  # type: ignore[attr-defined]

from .column import ColumnDefinition
from .schema import Schema


@dataclass(frozen=True)
class SchemaMatch:
    schema: Schema
    matching_columns: frozendict[str, ColumnDefinition]


def find_best_matching_schemas(
    schemas: Set[Schema], columns: Set[str]
) -> List[SchemaMatch]:
    """
    Find all schemas from the given set of schemas that match the given set of columns and return them ordered by best
    match

    Schemas that don't match at all (are missing required columns) will not be returned.
    """
    matches = []
    for schema in schemas:
        schema_match = schema.match_columns(columns)
        if schema_match.matches:
            matches.append(SchemaMatch(schema, schema_match.matching_columns))
    matches.sort(key=lambda match: len(match.matching_columns), reverse=True)
    return matches


def find_matching_schemas(schemas: Set[Schema], columns: Set[str]) -> Set[Schema]:
    """
    Find all schemas from the given set of schemas that match the given set of columns

    See `find_best_matching_schemas` if you care about best matches"""
    return {match.schema for match in find_best_matching_schemas(schemas, columns)}


class AmbigiousMatch(Exception):
    """Exception thrown when the best schema match for a set of columns is ambigious"""

    def __init__(self, matches: List[SchemaMatch]):
        self.matches = frozenset(matches)


def find_best_matching_schema(
    schemas: Set[Schema], columns: Set[str]
) -> Optional[Schema]:
    """
    Find the one best matching schema for the given set of columns

    Will throw AmbigiousMatch if there is more than one schema with the same number of matching columns.
    """
    best_matches = find_best_matching_schemas(schemas, columns)
    if len(best_matches) == 0:
        return None

    matches = [best_matches[0]]
    best_number_of_columns = len(best_matches[0].matching_columns)
    for match in best_matches[1:]:
        # The best matches are already sorted by number of matching columns
        assert len(match.matching_columns) <= best_number_of_columns
        if len(match.matching_columns) == best_number_of_columns:
            matches.append(match)
        else:
            # The list is sorted by number of matching columns so we can stop searching once we find one with fewer
            # matching columns
            break

    if len(matches) > 1:
        raise AmbigiousMatch(matches)

    return matches[0].schema
