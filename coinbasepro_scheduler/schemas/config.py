from typing import List, Optional

from pydantic import BaseModel

from coinbasepro_scheduler.schemas.alert import DiscordAlert
from coinbasepro_scheduler.schemas.api import CoinbaseProAPI
from coinbasepro_scheduler.schemas.scheduler import Scheduler


class Config(BaseModel):
    api: CoinbaseProAPI
    schedulers: List[Scheduler]
    discord: Optional[DiscordAlert]
