from datetime import datetime

from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    api_version: str
    message: str
    time: datetime
