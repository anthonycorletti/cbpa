from enum import Enum, unique

from pydantic import BaseModel
from pydantic.types import PositiveInt, StrictBool, StrictStr

from coinbasepro_scheduler.schemas.currency import FCC


@unique
class FundSource(str, Enum):
    default = "default"
    coinbase = "coinbase"


@unique
class AddFundsStatus(str, Enum):
    Success = "Success"
    Error = "Error"


class Account(BaseModel):
    auto_funding_enabled: StrictBool = True
    auto_funding_limit: PositiveInt
    fiat_currency: FCC = FCC.USD
    source: FundSource = FundSource.default


class AddFundsResponse(BaseModel):
    status: AddFundsStatus
    message: StrictStr
