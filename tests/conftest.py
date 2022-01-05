import os

import pytest

from cbpa.services.config import ConfigService

os.environ["TZ"] = "UTC"
config_service = ConfigService()


@pytest.fixture(scope="function", autouse=True)
def _function() -> None:
    pass
