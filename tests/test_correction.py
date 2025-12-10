import pytest
from pricing.correction import calculate_reference_price, correct_prices
from pricing.validation import validate_prices


def test_calculate_reference_mtpl():
    """MTPL reference price should be 400€"""
    price = calculate_reference_price("mtpl", None, None)
    assert price == 400


def test_calculate_reference_limited_casco_basic():
    """Limited Casco Basic 100€ should be 700€ (base)"""
    price = calculate_reference_price("limited_casco", "basic", 100)
    assert price == 700


def test_calculate_reference_with_variant():
    """Comfort variant should add 7%"""
    # Limited Casco Comfort 100 = 700 × 1.07 = 749
    price = calculate_reference_price("limited_casco", "comfort", 100)
    assert price == pytest.approx(749, rel=0.01)
    
    # Premium should add 14%
    price = calculate_reference_price("limited_casco", "premium", 100)
    assert price == pytest.approx(798, rel=0.01)


def test_calculate_reference_with_deductible():
    """Higher deductible should reduce price by 10% per step"""
    base = calculate_reference_price("casco", "basic", 100)  # 900
    with_200 = calculate_reference_price("casco", "basic", 200)  # 810
    with_500 = calculate_reference_price("casco", "basic", 500)  # 720
    
    assert base == 900
    assert with_200 == pytest.approx(810, rel=0.01)
    assert with_500 == pytest.approx(720, rel=0.01)


def test_calculate_reference_combined():
    """Test variant + deductible combined"""
    # Casco Premium 500 = 900 × 1.14 × 0.80
    price = calculate_reference_price("casco", "premium", 500)
    expected = 900 * 1.14 * 0.80
    assert price == pytest.approx(expected, rel=0.01)


def test_correct_prices_fixes_casco_too_low():
    """Correct prices should fix Casco being cheaper than Limited Casco"""
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 820,
        "casco_basic_100": 750,  # Too low
    }
    
    corrected = correct_prices(prices)
    
    # Casco should now be more expensive than Limited Casco
    assert corrected["casco_basic_100"] > corrected["limited_casco_basic_100"]
    
    # Should have no validation issues
    issues = validate_prices(corrected)
    assert len(issues) == 0


def test_correct_prices_fixes_variant_order():
    """Correct prices should fix variant ordering"""
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 800,
        "limited_casco_comfort_100": 750,  # Should be higher than compact
    }
    
    corrected = correct_prices(prices)
    
    # Comfort should be more expensive than compact
    assert corrected["limited_casco_comfort_100"] > corrected["limited_casco_compact_100"]


def test_correct_prices_fixes_deductible_order():
    """Correct prices should fix deductible ordering"""
    prices = {
        "mtpl": 400,
        "casco_basic_100": 700,
        "casco_basic_200": 750,  # Wrong - should be less than 100
    }
    
    corrected = correct_prices(prices)
    
    # 200€ deductible should be cheaper than 100€
    assert corrected["casco_basic_200"] < corrected["casco_basic_100"]

def test_correct_prices_preserves_valid():
    """Correction should not change already valid prices"""
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "casco_basic_100": 900,
    }
    
    # No issues in original
    issues = validate_prices(prices)
    assert len(issues) == 0
    
    # Correction should return same prices
    corrected = correct_prices(prices)
    assert corrected == prices

def test_correct_prices_with_valid_data():
    """Correction should handle already valid prices"""
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "casco_basic_100": 900,
    }
    
    corrected = correct_prices(prices)
    
    # Should have no violations
    issues = validate_prices(corrected)
    assert len(issues) == 0

def test_correct_prices_with_example_data():
    """Test with assignment example data"""
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 820,
        "casco_compact_100": 750,  # Problem
        "casco_basic_100": 830,    # Problem
    }
    
    # Should have issues
    issues_before = validate_prices(prices)
    assert len(issues_before) > 0
    
    # Correct
    corrected = correct_prices(prices)
    
    # Should have fewer or no issues
    issues_after = validate_prices(corrected)
    assert len(issues_after) < len(issues_before)

def test_correction_converges():
    """Check that the correction does not enter an infinite loop"""
    prices = {
        "mtpl": 1000,  # Extremely bad prices
        "limited_casco_basic_100": 100,
        "casco_basic_100": 50,
    }

    # It should not throw an exception
    corrected = correct_prices(prices)

    # It should converge toward valid prices
    issues = validate_prices(corrected)
    assert len(issues) == 0

def test_correct_prices_with_perfect_input():
    """If the prices are already perfect, don’t change anything"""
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "casco_basic_100": 900,
    }
    
    corrected = correct_prices(prices)
    
    # Prices should remain close to the original ones
    for key in prices:
        assert corrected[key] == pytest.approx(prices[key], rel=0.01)