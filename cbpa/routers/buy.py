from fastapi import APIRouter
from starlette.requests import Request

from cbpa.logger import logger
from cbpa.schemas.buy import BuyResponse

router = APIRouter()
tags = ["buy"]


@router.post("/buy", response_model=BuyResponse, tags=tags)
async def buy(request: Request) -> BuyResponse:
    logger.info("Buy API request initiated.")
    headers = request.headers
    logger.info(f"Received request: {headers}")
    logger.info("Buy API request completed.")
    return BuyResponse(message="Buy API request completed.")
