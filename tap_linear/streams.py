from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_linear.client import LinearStream

UserType = th.ObjectType(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("email", th.StringType),
)


class CyclesStream(LinearStream):
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
        th.Property("completedAt", th.DateTimeType),
        th.Property(
            "uncompletedIssuesUponClose",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("identifier", th.StringType),
                )
            ),
        ),
    ).to_dict()
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"

    def get_query(self, context: t.Optional[dict] = None) -> str:
        return """
        query Cycles($after: String, $filter: CycleFilter) {
            cycles(first: 100, after: $after, filter: $filter) {
                nodes {
                    id
                    name
                    description
                    team { id name key }
                    startsAt
                    endsAt
                    progress
                    updatedAt
                    completedAt
                    uncompletedIssuesUponClose { nodes { id identifier } }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """


class IssuesStream(LinearStream):
    name = "issues"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("identifier", th.StringType),
        th.Property("title", th.StringType),
        th.Property("description", th.StringType),
        th.Property("priority", th.NumberType),
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
        th.Property("cycle", th.ObjectType(th.Property("id", th.StringType))),
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
                )
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
                        "issue", th.ObjectType(th.Property("id", th.StringType))
                    ),
                    th.Property("actor", UserType),
                    th.Property("fromCycleId", th.StringType),
                    th.Property("toCycleId", th.StringType),
                    th.Property("toAssigneeId", th.StringType),
                    th.Property("fromStateId", th.StringType),
                    th.Property("toStateId", th.StringType),
                )
            ),
        ),
    ).to_dict()
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"

    def get_query(self, context: t.Optional[dict] = None) -> str:
        return """
        query Issues($after: String, $filter: IssueFilter) {
            issues(first: 35, after: $after, filter: $filter, includeArchived: true) {
                nodes {
                    id
                    identifier
                    title
                    description
                    priority
                    state { id name type }
                    estimate
                    createdAt
                    updatedAt
                    completedAt
                    archivedAt
                    cycle { id }
                    assignee { id name email }
                    creator { id name email }
                    team { id name key }
                    project { id name }
                    parent { id title }
                    labels { nodes { id name color } }
                    history { nodes {
                        id
                        createdAt
                        updatedAt
                        issue { id }
                        actor { id }
                        fromCycleId
                        toCycleId
                        fromAssigneeId
                        toAssigneeId
                        fromStateId
                        toStateId
                    } }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """


class CommentStream(LinearStream):
    name = "comments"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("user", UserType),
        th.Property("issue", th.ObjectType(th.Property("id", th.StringType))),
        th.Property("body", th.StringType),
    ).to_dict()
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"

    def get_query(self, context: t.Optional[dict] = None) -> str:
        return """
        query Comments($after: String, $filter: CommentFilter) {
            comments(first: 100, after: $after, filter: $filter) {
                nodes {
                    id
                    createdAt
                    updatedAt
                    user { id name email }
                    issue { id }
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

    def get_query(self, context: t.Optional[dict] = None) -> str:
        return """
        query Users($after: String, $filter: UserFilter) {
            users(first: 100, after: $after, filter: $filter, includeArchived: true, includeDisabled: true) {
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


class WorkflowStateStream(LinearStream):
    name = "workflowStates"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),
        th.Property("color", th.StringType),
        th.Property("position", th.NumberType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("description", th.StringType),
    ).to_dict()
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "updatedAt"

    def get_query(self, context: t.Optional[dict] = None) -> str:
        return """
        query WorkflowStates($after: String, $filter: WorkflowStateFilter) {
            workflowStates(first: 100, after: $after, filter: $filter, includeArchived: true) {
                nodes {
                    id
                    color
                    createdAt
                    description
                    name
                    position
                    type
                    updatedAt
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
        """
