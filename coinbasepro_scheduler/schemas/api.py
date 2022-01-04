from pydantic import BaseModel, SecretStr, StrictStr


class CoinbaseProAPI(BaseModel):
    key: SecretStr
    secret: SecretStr
    passphrase: SecretStr
    url: StrictStr = "https://api.pro.coinbase.com"
