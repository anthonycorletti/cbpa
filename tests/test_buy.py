from coinbasepro_scheduler.schemas.buy import Buy


def test_pair() -> None:
    buy = Buy(send_currency="USD", send_amount=1, receive_currency="BTC")
    assert buy.pair() == "BTC-USD"
    assert buy.pair() != "USD-BTC"
