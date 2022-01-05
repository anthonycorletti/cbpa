from typing import List, Optional

from pydantic import BaseModel

from cbpa.schemas.account import Account
from cbpa.schemas.alert import DiscordAlert
from cbpa.schemas.api import CoinbaseProAPI
from cbpa.schemas.buy import Buy


class Config(BaseModel):
    api: CoinbaseProAPI
    account: Account
    discord: Optional[DiscordAlert]
    buys: List[Buy]
