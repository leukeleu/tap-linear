"""Stream type classes for tap-linear."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_linear.client import LinearStream


class CyclesStream(LinearStream):
    """Cycle stream."""
    name = "cycles"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property(
            "team",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("key", th.StringType),
            ),
        ),
        th.Property("startsAt", th.DateTimeType),
        th.Property("endsAt", th.DateTimeType),
        th.Property("progress", th.NumberType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property(
            "uncompletedIssuesUponClose",
            th.ObjectType(
                th.Property(
                    "nodes",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("id", th.StringType),
                            th.Property("identifier", th.StringType),
                        ),
                    ),
                ),
            ),
        ),
    ).to_dict()

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"
    query = """
        query Cycles($next: String, $replicationKeyValue: DateTime) {
            cycles(
                first: 100
                after: $next
                filter: { updatedAt: {gt: $replicationKeyValue } }
            ) {
                nodes {
                    id
                    name
                    description
                    team {
                        id
                        name
                        key
                    }
                    startsAt
                    endsAt
                    progress
                    updatedAt
                    uncompletedIssuesUponClose {
                      nodes {
                            id
                            identifier
                        }
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """
