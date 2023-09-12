"""GraphQL client handling, including LinearStream base class."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.streams import GraphQLStream


class LinearStream(GraphQLStream):
    """Linear stream class."""

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator(
            self,
            key="Authorization",
            value=self.config.get("auth_token"),
        )

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("api_url")

    @classproperty
    def records_jsonpath(cls) -> str:  # noqa: N805
        """Return the JSON path to the list of records for the stream."""
        return f"$.data.{cls.name}.nodes[*]"

    @classproperty
    def next_page_token_jsonpath(cls) -> str:  # noqa: N805
        """Return the JSON path to the next page token for the stream."""
        return f"$.data.{cls.name}.pageInfo.endCursor"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, Any] | str:
        """Return the URL params needed.

        These URL params are actually GraphQL variables.

        Args:
            context: The context dictionary.
            next_page_token: The next page token.

        Returns:
            A dictionary of URL params.
        """
        next_second = self.get_starting_timestamp(context) + timedelta(seconds=1)
        return {
            "next": next_page_token,
            "replicationKeyValue": next_second.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }