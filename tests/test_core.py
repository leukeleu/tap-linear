"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing.legacy import get_standard_tap_tests

from tap_linear.tap import TapLinear

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "auth_token": "test",
}


def test_standard_tap_tests(requests_mock) -> None:  # noqa: ANN001
    """Run standard built-in tap tests from the SDK."""
    requests_mock.post("/graphql", json={"data": {"results": {"nodes": []}}})
    tests = get_standard_tap_tests(TapLinear, config=SAMPLE_CONFIG)
    for test in tests:
        test()
