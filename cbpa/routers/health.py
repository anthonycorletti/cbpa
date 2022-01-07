from datetime import datetime

from fastapi import APIRouter

from cbpa import __version__
from cbpa.logger import logger
from cbpa.schemas.health import HealthcheckResponse

router = APIRouter()
tags = ["health"]


@router.get("/healthcheck", response_model=HealthcheckResponse, tags=tags)
def healthcheck() -> HealthcheckResponse:
    message = "Dollar cost averaging."
    logger.debug(message)
    return HealthcheckResponse(
        api_version=__version__,
        message=message,
        time=datetime.now(),
    )
