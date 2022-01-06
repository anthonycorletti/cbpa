import os
from typing import Generator

import pytest
from typer.testing import CliRunner

os.environ["TZ"] = "UTC"


@pytest.fixture(scope="function")
def cli_runner() -> Generator:
    yield CliRunner()
