import pytest
from pricing.correction import correct_prices
from pricing.validation import validate_prices


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