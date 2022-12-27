from typing import Set

from .schema import Schema


def find_matching_schemas(schemas: Set[Schema], columns: Set[str]) -> Set[Schema]:
    """Find all schemas from the given set of schemas that match the given set of columns"""
    return {schema for schema in schemas if schema.columns_match(columns)}
