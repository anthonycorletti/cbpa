from pydantic import BaseModel, StrictStr


class DiscordAlert(BaseModel):
    webhook: StrictStr
