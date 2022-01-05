from enum import Enum, unique

from pydantic import BaseModel, PositiveInt, StrictStr

from cbpa.schemas.currency import FCC


@unique
class AddFundsStatus(str, Enum):
    Success = "Success"
    Error = "Error"


class Account(BaseModel):
    auto_funding_limit: PositiveInt
    fiat_currency: FCC = FCC.USD


class AddFundsResponse(BaseModel):
    status: AddFundsStatus
    message: StrictStr
