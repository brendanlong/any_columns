from dataclasses import dataclass
from typing import FrozenSet, List, Optional, Set

from .column import Column
from .schema import Schema


def find_matching_schemas(schemas: Set[Schema], columns: Set[str]) -> Set[Schema]:
    """
    Find all schemas from the given set of schemas that match the given set of columns

    See `find_best_matching_schemas` if you care about best matches"""
    return {schema for schema in schemas if schema.columns_match(columns)}


@dataclass(frozen=True)
class SchemaMatch:
    """
    A schema and the columns that it matched in the given columns

    This can be used to determine which schema is the best match for an input.
    """

    schema: Schema
    matching_columns: FrozenSet[Column]


def find_best_matching_schemas(
    schemas: Set[Schema], columns: Set[str]
) -> List[SchemaMatch]:
    """
    Find all schemas from the given set of schemas that match the given set of columns and return them ordered by best
    match

    Schemas that don't match at all (are missing required columns) will not be returned.
    """
    matching_schemas = find_matching_schemas(schemas, columns)
    matching_schemas_with_columns = [
        SchemaMatch(schema, frozenset(schema.matching_columns(columns)))
        for schema in matching_schemas
    ]
    matching_schemas_with_columns.sort(
        key=lambda match: len(match.matching_columns), reverse=True
    )
    return matching_schemas_with_columns


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
