import pytest
from pricing.parsing import parse_price_key


def test_parse_mtpl():
    product, variant, deductible = parse_price_key("mtpl")
    assert product == "mtpl"
    assert variant is None
    assert deductible is None


def test_parse_limited_casco():
    product, variant, deductible = parse_price_key("limited_casco_comfort_200")
    assert product == "limited_casco"
    assert variant == "comfort"
    assert deductible == 200


def test_parse_casco():
    product, variant, deductible = parse_price_key("casco_premium_500")
    assert product == "casco"
    assert variant == "premium"
    assert deductible == 500


def test_invalid_key_format():
    with pytest.raises(ValueError, match="Unexpected key format"):
        parse_price_key("invalid_key")


def test_invalid_deductible():
    with pytest.raises(ValueError, match="Invalid deductible"):
        parse_price_key("casco_basic_abc")