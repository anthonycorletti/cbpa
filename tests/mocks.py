import uuid
from typing import Dict, List


class MockCoinbaseClient:
    def get_accounts(self) -> List[Dict]:
        return [{"balance": 100, "currency": "USD"}]

    def get_payment_methods(self) -> List[Dict]:
        return [
            {
                "id": "900229be-9eb0-4e54-96b2-6a7ccf2a7c51",
                "primary_buy": True,
                "currency": "USD",
            }
        ]

    def deposit(self, amount: float, currency: str, payment_method_id: str) -> None:
        return None

    def place_market_order(self, product_id: str, side: str, funds: float) -> Dict:
        return {"id": str(uuid.uuid4())}

    def get_order(self, order_id: str) -> Dict:
        return {"filled_size": 2}
