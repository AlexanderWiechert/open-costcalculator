from core import pricing_utils

def test_get_price_for_service_fallback():
    mock_client = type("MockClient", (), {
        "get_products": lambda self, **kwargs: {"PriceList": []}
    })()
    price = pricing_utils.get_price_for_service(mock_client, "AmazonEC2", [], fallback_price=0.123)
    assert price == 0.123
