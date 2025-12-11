from pricing.validation import validate_prices


def test_mtpl_vs_limited_casco_violation():
    prices = {
        "mtpl": 450, 
        "limited_casco_basic_100": 420,
        "casco_basic_100": 900,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("MTPL" in issue and "Limited Casco" in issue for issue in issues)


def test_limited_casco_vs_casco_violation():
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 950, 
        "casco_basic_100": 900,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("Limited Casco" in issue and "Casco" in issue for issue in issues)


def test_compact_vs_comfort_violation():
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 800,  
        "limited_casco_comfort_100": 750,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("compact" in issue and "comfort" in issue for issue in issues)


def test_basic_vs_comfort_violation():
    prices = {
        "mtpl": 400,
        "casco_basic_100": 900,  
        "casco_comfort_100": 850,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("basic" in issue and "comfort" in issue for issue in issues)


def test_comfort_vs_premium_violation():
    prices = {
        "mtpl": 400,
        "limited_casco_comfort_100": 1000, 
        "limited_casco_premium_100": 950,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("comfort" in issue and "premium" in issue for issue in issues)


def test_deductible_100_vs_200_violation():
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "limited_casco_basic_200": 750,  
        "casco_basic_100": 900,
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("deductible 100" in issue and "deductible 200" in issue for issue in issues)


def test_deductible_200_vs_500_violation():
    prices = {
        "mtpl": 400,
        "casco_basic_200": 800,
        "casco_basic_500": 850,  
    }
    issues = validate_prices(prices)
    assert len(issues) > 0
    assert any("deductible 200" in issue and "deductible 500" in issue for issue in issues)



def test_valid_prices_no_issues():
    prices = {
        "mtpl": 400,
        "limited_casco_basic_100": 700,
        "limited_casco_basic_200": 630,  
        "limited_casco_basic_500": 560, 
        "casco_basic_100": 900,
        "casco_basic_200": 810,
        "casco_basic_500": 720,
    }
    issues = validate_prices(prices)
    assert len(issues) == 0


def test_valid_variant_ordering():
    prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 700,
        "limited_casco_comfort_100": 749, 
        "limited_casco_premium_100": 798,  
    }
    issues = validate_prices(prices)
    assert len(issues) == 0


def test_multiple_violations():
    prices = {
        "mtpl": 450,  
        "limited_casco_basic_100": 420,
        "limited_casco_basic_200": 450,  
        "casco_basic_100": 400,  
    }
    issues = validate_prices(prices)
    assert len(issues) >= 3


def test_empty_prices():
    prices = {}
    issues = validate_prices(prices)
    assert len(issues) == 0  


def test_only_mtpl():
    prices = {"mtpl": 400}
    issues = validate_prices(prices)
    assert len(issues) == 0  