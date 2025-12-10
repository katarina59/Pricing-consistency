from pricing.validation import validate_prices


def test_mtpl_vs_limited_casco_violation():
    """MTPL must be cheaper than Limited Casco"""
    prices = {
        "mtpl": 450,  # VIOLATION: too expensive
        "limited_casco_basic_100": 420,
        "casco_basic_100": 900,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("MTPL" in issue and "Limited Casco" in issue for issue in issues)


def test_limited_casco_vs_casco_violation():
    """Limited Casco must be cheaper than Casco (for the same variant/deductible)"""
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 950,  # VIOLATION: more expensive than Casco
        "casco_basic_100": 900,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("Limited Casco" in issue and "Casco" in issue for issue in issues)


def test_compact_vs_comfort_violation():
    """Compact must be cheaper than Comfort"""
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 800,  # VIOLATION: more expensive than Comfort
        "limited_casco_comfort_100": 750,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("compact" in issue and "comfort" in issue for issue in issues)


def test_basic_vs_comfort_violation():
    """Basic must be cheaper than Comfort"""
    prices = {
        "mtpl": 400,
        "casco_basic_100": 900,  # VIOLATION: more expensive than Comfort
        "casco_comfort_100": 850,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("basic" in issue and "comfort" in issue for issue in issues)


def test_comfort_vs_premium_violation():
    """Comfort must be cheaper than Premium"""
    prices = {
        "mtpl": 400,
        "limited_casco_comfort_100": 1000,  # VIOLATION: more expensive than Premium
        "limited_casco_premium_100": 950,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("comfort" in issue and "premium" in issue for issue in issues)


def test_deductible_100_vs_200_violation():
    """100€ deductible must be more expensive than 200€"""
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "limited_casco_basic_200": 750,  # VIOLATION: more expensive than 100
        "casco_basic_100": 900,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("deductible 100" in issue and "deductible 200" in issue for issue in issues)


def test_deductible_200_vs_500_violation():
    """200€ deductible must be more expensive than 500€"""
    prices = {
        "mtpl": 400,
        "casco_basic_200": 800,
        "casco_basic_500": 850,  # VIOLATION: more expensive than 200
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("deductible 200" in issue and "deductible 500" in issue for issue in issues)



def test_valid_prices_no_issues():
    """Valid prices should not have any errors"""
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "limited_casco_basic_200": 630,  # 10% cheaper
        "limited_casco_basic_500": 560,  # another 10% cheaper
        "casco_basic_100": 900,
        "casco_basic_200": 810,
        "casco_basic_500": 720,
    }
    issues = validate_prices(prices)
    assert len(issues) == 0


def test_valid_variant_ordering():
    """Tests valid comparison of variants"""
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 700,
        "limited_casco_comfort_100": 749,  # 7% higher
        "limited_casco_premium_100": 798,  # 14% higher
    }
    issues = validate_prices(prices)
    assert len(issues) == 0


def test_multiple_violations():
    """Tests a scenario with multiple different errors"""
    prices = {
        "mtpl": 450,  # Too expensive vs Limited Casco
        "limited_casco_basic_100": 420,
        "limited_casco_basic_200": 450,  # Too expensive vs 100
        "casco_basic_100": 400,  # Too cheap vs Limited Casco
    }
    issues = validate_prices(prices)
    # We expect at least 3 errors
    assert len(issues) >= 3


def test_empty_prices():
    """Test with an empty dictionary"""
    prices = {}
    issues = validate_prices(prices)
    assert len(issues) == 0  # No prices = no errors


def test_only_mtpl():
    """Test with only MTPL without other products"""
    prices = {"mtpl": 400}
    issues = validate_prices(prices)
    assert len(issues) == 0  # You can’t violate rules if there’s nothing to compare