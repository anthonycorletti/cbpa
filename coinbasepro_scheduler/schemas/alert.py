from typing import Dict, Optional

from pydantic import BaseModel, validator
from pydantic.types import StrictBool, StrictStr


class DiscordAlert(BaseModel):
    enabled: StrictBool = False
    webhook: Optional[StrictStr] = None

    @validator("webhook", pre=True, always=True)
    def validate_webhook_set_if_enabled(
        cls: BaseModel, v: Optional[StrictStr], values: Dict
    ) -> Optional[str]:
        if values["enabled"] and not v:
            raise ValueError("DiscordAlert enabled but webhook url not set.")
        return v
