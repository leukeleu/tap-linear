"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_linear.tap import TapLinear

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d"),
    "auth_token": "test",
}


# Run standard built-in tap tests from the SDK:
TestTapLinear = get_tap_test_class(
    tap_class=TapLinear,
    config=SAMPLE_CONFIG,
)
