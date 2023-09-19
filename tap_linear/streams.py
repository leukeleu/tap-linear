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
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("identifier", th.StringType),
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
                filter: { updatedAt: { gt: $replicationKeyValue } }
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


UserType = th.ObjectType(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("email", th.StringType),
)


class IssuesStream(LinearStream):
    """Issues stream."""

    name = "issues"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("identifier", th.StringType),
        th.Property("title", th.StringType),
        th.Property("description", th.StringType),
        th.Property("priority", th.NumberType),
        th.Property("type", th.StringType),
        th.Property(
            "state",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("type", th.StringType),
            ),
        ),
        th.Property("estimate", th.NumberType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("completedAt", th.DateTimeType),
        th.Property("archivedAt", th.DateTimeType),
        th.Property("assignee", UserType),
        th.Property("creator", UserType),
        th.Property(
            "team",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("key", th.StringType),
            ),
        ),
        th.Property(
            "project",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("key", th.StringType),
            ),
        ),
        th.Property(
            "parent",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("title", th.StringType),
            ),
        ),
        th.Property(
            "labels",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("color", th.StringType),
                ),
            ),
        ),
        th.Property(
            "history",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("createdAt", th.DateTimeType),
                    th.Property("updatedAt", th.DateTimeType),
                    th.Property(
                        "issue",
                        th.ObjectType(
                            th.Property("id", th.StringType),
                        ),
                    ),
                    th.Property("actor", UserType),
                    th.Property("fromCycleId", th.StringType),
                    th.Property("toCycleId", th.StringType),
                    th.Property("toAssigneeId", th.StringType),
                    th.Property("fromStateId", th.StringType),
                    th.Property("toStateId", th.StringType),
                ),
            ),
        ),
    ).to_dict()

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"
    query = """
        query Issues($next: String, $replicationKeyValue: DateTime) {
            issues(
                first: 35
                after: $next
                filter: { updatedAt: { gt: $replicationKeyValue } }
            ) {
                nodes {
                    id
                    identifier
                    title
                    description
                    priority
                    state {
                        id
                        name
                        type
                    }
                    estimate
                    createdAt
                    updatedAt
                    completedAt
                    archivedAt
                    assignee {
                        id
                        name
                        email
                    }
                    creator {
                        id
                        name
                        email
                    }
                    team {
                        id
                        name
                        key
                    }
                    project {
                        id
                        name
                    }
                    parent {
                        id
                        title
                    }
                    labels {
                        nodes {
                            id
                            name
                            color
                        }
                    }
                    history {
                        nodes {
                            id
                            createdAt
                            updatedAt
                            issue {
                                id
                            }
                            actor {
                                id
                            }
                            fromCycleId
                            toCycleId
                            toAssigneeId
                            fromStateId
                            toStateId
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


class CommentStream(LinearStream):
    """Comment stream."""

    name = "comments"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("user", UserType),
        th.Property(
            "issue",
            th.ObjectType(
                th.Property("id", th.StringType),
            ),
        ),
    ).to_dict()

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"
    query = """
        query Comments($next: String, $replicationKeyValue: DateTime) {
            comments(
                first: 100
                after: $next
                filter: { updatedAt: { gt: $replicationKeyValue } }
            ) {
                nodes {
                    id
                    createdAt
                    updatedAt
                    user {
                        id
                        name
                        email
                    }
                    issue {
                        id
                    }
                    body
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """


class UsersStream(LinearStream):
    """Users stream."""

    name = "users"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("displayName", th.StringType),
        th.Property("email", th.StringType),
        th.Property("guest", th.BooleanType),
        th.Property("lastSeen", th.DateTimeType),
        th.Property("name", th.StringType),
    ).to_dict()

    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"
    query = """
        query Users($next: String, $replicationKeyValue: DateTime) {
            users(
                first: 100
                after: $next
                filter: { updatedAt: { gt: $replicationKeyValue } }
            ) {
                nodes {
                    id
                    active
                    createdAt
                    updatedAt
                    displayName
                    email
                    guest
                    lastSeen
                    name
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """
