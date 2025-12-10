import pytest
from pricing.parsing import parse_price_key


def test_parse_mtpl():
    """Parse basic MTPL product"""
    product, variant, deductible = parse_price_key("mtpl")
    assert product == "mtpl"
    assert variant is None
    assert deductible is None


def test_parse_limited_casco():
    """Parse Limited Casco with variant and deductible"""
    product, variant, deductible = parse_price_key("limited_casco_comfort_200")
    assert product == "limited_casco"
    assert variant == "comfort"
    assert deductible == 200


def test_parse_casco():
    """Parse Casco with variant and deductible"""
    product, variant, deductible = parse_price_key("casco_premium_500")
    assert product == "casco"
    assert variant == "premium"
    assert deductible == 500


def test_parse_all_variants():
    """Test all variant types"""
    variants = ["compact", "basic", "comfort", "premium"]
    for v in variants:
        product, variant, deductible = parse_price_key(f"casco_{v}_100")
        assert product == "casco"
        assert variant == v
        assert deductible == 100


def test_parse_all_deductibles():
    """Test all deductible amounts"""
    deductibles = [100, 200, 500]
    for d in deductibles:
        product, variant, deductible = parse_price_key(f"limited_casco_basic_{d}")
        assert product == "limited_casco"
        assert variant == "basic"
        assert deductible == d


def test_invalid_key_format():
    """Should raise error for invalid format"""
    with pytest.raises(ValueError, match="Unexpected key format"):
        parse_price_key("invalid_key")


def test_invalid_deductible():
    """Should raise error for non-numeric deductible"""
    with pytest.raises(ValueError, match="Invalid deductible"):
        parse_price_key("casco_basic_abc")