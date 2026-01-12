from typing import Optional, Tuple, Dict


# Parses a price dictionary key into its components (product, variant, deductible).
# Handles special case for "mtpl" and extracts product name, variant name, and deductible value from keys like "limited_casco_comfort_100"
def parse_price_key(key: str) -> Tuple[str, Optional[str], Optional[int]]:

    if key == "mtpl":
        return "mtpl", None, None
    
    parts = key.split("_")
    
    if len(parts) < 3:
        raise ValueError(f"Unexpected key format: {key}")
    
    product = "_".join(parts[:-2])
    variant = parts[-2]
    deductible_str = parts[-1]
    
    try:
        deductible = int(deductible_str)
    except ValueError:
        raise ValueError(f"Invalid deductible value in key: {key}")
    
    return product, variant, deductible

# Transforms a flat prices dictionary into a nested structure for easier navigation
# Groups prices by product, variant, and deductible ("limited_casco_comfort_100" becomes structured["limited_casco"]["comfort"][100])
def build_structured(prices: Dict[str, float]) -> Dict:
    structured = {}
    for key, price in prices.items():
        product, variant, deductible = parse_price_key(key)
        
        if product not in structured:
            structured[product] = {}
        if variant not in structured[product]:
            structured[product][variant] = {}
        
        structured[product][variant][deductible] = price
    
    return structured