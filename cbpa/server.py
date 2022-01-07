import os

import uvicorn
from fastapi import FastAPI

from cbpa import __version__
from cbpa.routers import buy, health

os.environ["TZ"] = "UTC"

api = FastAPI(
    title="Coinbase Pro Automation API",
    description="Automate buys for your favourite cryptocurrencies.",
    version=__version__,
)

api.include_router(health.router)
api.include_router(buy.router)


def _run_server(port: int, host: str) -> None:
    uvicorn.run(api, port=port, host=host)
