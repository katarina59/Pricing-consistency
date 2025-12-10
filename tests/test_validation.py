from pricing.validation import validate_prices


def test_deductible_order_violation():
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "limited_casco_basic_200": 750,  # violation
        "limited_casco_basic_500": 650,
        "casco_basic_100": 900,
        "casco_basic_200": 850,
        "casco_basic_500": 800,
    }

    issues = validate_prices(prices)
    assert len(issues) > 0
