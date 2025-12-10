from typing import Dict
from pricing.validation import validate_prices
from pricing.correction import correct_prices


def analyze_and_fix_prices(prices: Dict[str, float]) -> Dict[str, float]:
    """
    Main function that validates and corrects insurance pricing.
    
    Args:
        prices: Dictionary of insurance prices
        
    Returns:
        Corrected prices dictionary
    """
    
    print("\n1. Validating original prices...")
    issues = validate_prices(prices)
    
    if issues:
        print(f"\n   Found {len(issues)} issue(s):")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("   No issues found - pricing is valid!")
        return prices
    
    print("\n2. Applying automatic corrections...")
    corrected_prices = correct_prices(prices)
    
    print("\n3. Validating corrected prices...")
    remaining_issues = validate_prices(corrected_prices)
    
    if remaining_issues:
        print(f"\n   Still {len(remaining_issues)} issue(s) remaining:")
        for i, issue in enumerate(remaining_issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("   All issues resolved!")
    
    print("\n4. Price changes:")
    changes_made = False
    for key in prices:
        if prices[key] != corrected_prices[key]:
            changes_made = True
            print(f"   {key}: {prices[key]:.2f} → {corrected_prices[key]:.2f}")
    
    if not changes_made:
        print("   No changes needed")
    
    print("\n" + "=" * 60)
    
    return corrected_prices


if __name__ == "__main__":
    example_prices = {
        "mtpl": 400,
        "limited_casco_compact_100": 820,
        "limited_casco_compact_200": 760,
        "limited_casco_compact_500": 650,
        "limited_casco_basic_100": 900,
        "limited_casco_basic_200": 780,
        "limited_casco_basic_500": 600,
        "limited_casco_comfort_100": 950,
        "limited_casco_comfort_200": 870,
        "limited_casco_comfort_500": 720,
        "limited_casco_premium_100": 1100,
        "limited_casco_premium_200": 980,
        "limited_casco_premium_500": 800,
        "casco_compact_100": 750,
        "casco_compact_200": 700,
        "casco_compact_500": 620,
        "casco_basic_100": 830,
        "casco_basic_200": 760,
        "casco_basic_500": 650,
        "casco_comfort_100": 900,
        "casco_comfort_200": 820,
        "casco_comfort_500": 720,
        "casco_premium_100": 1050,
        "casco_premium_200": 950,
        "casco_premium_500": 780
    }
    
    corrected = analyze_and_fix_prices(example_prices)