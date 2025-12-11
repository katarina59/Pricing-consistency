import pytest
from pricing.correction import calculate_reference_price, correct_prices
from pricing.validation import validate_prices


def test_calculate_reference_mtpl():
    price = calculate_reference_price("mtpl", None, None)
    assert price == 400


def test_calculate_reference_limited_casco_basic():
    price = calculate_reference_price("limited_casco", "basic", 100)
    assert price == 700


def test_calculate_reference_with_variant():
    price = calculate_reference_price("limited_casco", "comfort", 100)
    assert price == pytest.approx(749, rel=0.01)
    
    price = calculate_reference_price("limited_casco", "premium", 100)
    assert price == pytest.approx(798, rel=0.01)


def test_calculate_reference_with_deductible():
    base = calculate_reference_price("casco", "basic", 100)  
    with_200 = calculate_reference_price("casco", "basic", 200)  
    with_500 = calculate_reference_price("casco", "basic", 500)  
    
    assert base == 900
    assert with_200 == pytest.approx(810, rel=0.01)
    assert with_500 == pytest.approx(720, rel=0.01)


def test_correct_prices_fixes_casco_too_low():
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 820,
        "casco_basic_100": 750, 
    }
    
    corrected = correct_prices(prices)
    
    assert corrected["casco_basic_100"] > corrected["limited_casco_basic_100"]
    
    issues = validate_prices(corrected)
    assert len(issues) == 0


def test_correct_prices_fixes_variant_order():
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 800,
        "limited_casco_comfort_100": 750,  
    }
    
    corrected = correct_prices(prices)
    
    assert corrected["limited_casco_comfort_100"] > corrected["limited_casco_compact_100"]


def test_correct_prices_fixes_deductible_order():
    prices = {
        "mtpl": 400,
        "casco_basic_100": 700,
        "casco_basic_200": 750,  
    }
    
    corrected = correct_prices(prices)
    
    assert corrected["casco_basic_200"] < corrected["casco_basic_100"]


def test_correct_prices_with_example_data():
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 820,
        "casco_compact_100": 750,  
        "casco_basic_100": 830,    
    }
    
    issues_before = validate_prices(prices)
    assert len(issues_before) > 0
    
    corrected = correct_prices(prices)
    
    issues_after = validate_prices(corrected)
    assert len(issues_after) < len(issues_before)

def test_correction_converges():
    prices = {
        "mtpl": 1000,  
        "limited_casco_basic_100": 100,
        "casco_basic_100": 50,
    }

    corrected = correct_prices(prices)

    issues = validate_prices(corrected)
    assert len(issues) == 0

def test_correct_prices_with_perfect_input():
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "casco_basic_100": 900,
    }
    
    corrected = correct_prices(prices)
    
    for key in prices:
        assert corrected[key] == pytest.approx(prices[key], rel=0.01)