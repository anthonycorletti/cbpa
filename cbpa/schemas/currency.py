from enum import Enum, unique


@unique
class CCC(str, Enum):
    """CCC stands for _C_rypto_C_urrency _C_ode"""

    BTC = "BTC"
    ETH = "ETH"
    DOGE = "DOGE"
    SHIB = "SHIB"
    MANA = "MANA"
    AVAX = "AVAX"
    SOL = "SOL"
    XTZ = "XTZ"


@unique
class FCC(str, Enum):
    """FCC stands for _F_iat _C_urrency _C_ode"""

    USD = "USD"
