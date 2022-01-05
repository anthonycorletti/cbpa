from pydantic import BaseModel
from pydantic.types import PositiveInt

from cbpa.schemas.currency import CCC, FCC


class Buy(BaseModel):
    send_currency: FCC = FCC.USD
    send_amount: PositiveInt
    receive_currency: CCC

    def pair(self) -> str:
        return f"{self.receive_currency}-{self.send_currency}"
