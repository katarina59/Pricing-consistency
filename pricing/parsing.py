from typing import Optional, Tuple, Dict


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