from __future__ import annotations

import copy
import logging

from typing import Any, Dict, Iterable, Optional

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.exceptions import FatalAPIError
from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.streams import GraphQLStream

from tap_linear.utils import flatten_node_lists


class LinearStream(GraphQLStream):
    """Linear stream class."""

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator(
            self, key="Authorization", value=self.config.get("auth_token")
        )

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("api_url")

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return the URL params needed.

        These URL params are actually GraphQL variables.

        Args:
            context: The context dictionary.
            next_page_token: The next page token.

        Returns:
            A dictionary of URL params.
        """
        params: Dict[str, Any] = {}

        if next_page_token:
            params["after"] = next_page_token

        if self.replication_key and (
            starting_timestamp := self.get_starting_timestamp(context)
        ):
            params["filter"] = {
                self.replication_key: {"gt": starting_timestamp.isoformat()}
            }

        return {"variables": params}

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        query = self.get_query(context)
        variables = self.get_url_params(context, next_page_token)["variables"]
        return {
            "query": query,
            "variables": variables,
        }

    def parse_response(self, response: dict) -> Iterable[dict]:
        try:
            data = response["data"][self.name]["nodes"]
            for row in data:
                yield self.post_process(row)
        except KeyError as e:
            logging.error(f"Unexpected response structure: {response}")
            logging.error(f"KeyError: {e}")
            raise

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        try:
            return flatten_node_lists(row)
        except Exception as e:
            logging.error(f"Error in post_process: {e}")
            logging.error(f"Problematic row: {row}")
            return None

    def get_next_page_token(
        self, response: Dict[str, Any], previous_token: Optional[Any] = None
    ) -> Optional[Any]:
        try:
            has_next_page = response["data"][self.name]["pageInfo"]["hasNextPage"]
            if has_next_page:
                return response["data"][self.name]["pageInfo"]["endCursor"]
        except KeyError:
            logging.error(f"Unexpected response structure for pagination: {response}")
        return None

    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        next_page_token: Any = None
        finished = False
        while not finished:
            prepared_request = self.prepare_request(
                context, next_page_token=next_page_token
            )
            resp = self._request(prepared_request, context)
            for row in self.parse_response(resp):
                yield row
            previous_token = copy.deepcopy(next_page_token)
            next_page_token = self.get_next_page_token(resp, previous_token)
            if next_page_token and next_page_token == previous_token:
                raise RuntimeError(
                    f"Loop detected in pagination. Token {next_page_token} is identical to prior token."
                )
            finished = not next_page_token

    def _request(
        self, prepared_request, context: Optional[dict] = None
    ) -> Dict[str, Any]:
        response = self.requests_session.send(prepared_request)
        if response.status_code != 200:
            raise FatalAPIError(
                f"Request failed with status {response.status_code}: {response.text}"
            )
        return response.json()
