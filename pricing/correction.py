from typing import Dict, Optional
from pricing.parsing import parse_price_key, build_structured
from pricing.rules import (
    REFERENCE_PRICES,
    VARIANT_STEP_PERCENT,
    DEDUCTIBLE_STEP_PERCENT,
    VARIANT_ORDER,
    DEDUCTIBLE_ORDER,
)


def calculate_reference_price(
    product: str,
    variant: Optional[str],
    deductible: Optional[int]
) -> float:
    """
    Calculate reference price based on product, variant, and deductible.
    
    Formula:
        base_price × variant_multiplier × deductible_multiplier
    
    Args:
        product: Product type (mtpl, limited_casco, casco)
        variant: Variant type (None for mtpl, or compact/basic/comfort/premium)
        deductible: Deductible amount (None for mtpl, or 100/200/500)
        
    Returns:
        Calculated reference price in euros
    """
    base_price = REFERENCE_PRICES.get(product, 700)
    
    if variant is None or deductible is None:
        return base_price


    if variant in ["compact", "basic"]:
        variant_multiplier = 1.0
    elif variant == "comfort":
        variant_multiplier = 1.0 + VARIANT_STEP_PERCENT
    elif variant == "premium":
        variant_multiplier = 1.0 + 2 * VARIANT_STEP_PERCENT
    else:
        variant_multiplier = 1.0
    

    if deductible == 100:
        deductible_multiplier = 1.0
    elif deductible == 200:
        deductible_multiplier = 1.0 - DEDUCTIBLE_STEP_PERCENT
    elif deductible == 500:
        deductible_multiplier = 1.0 - 2 * DEDUCTIBLE_STEP_PERCENT
    else:
        deductible_multiplier = 1.0
    
    return base_price * variant_multiplier * deductible_multiplier


def correct_prices(prices: Dict[str, float]) -> Dict[str, float]:
    """
    Automatically correct pricing inconsistencies using reference values.
    
    Strategy:
    When a validation rule is violated, replace ALL involved prices
    with their reference values to ensure consistency.
    
    Args:
        prices: Original prices dictionary
        
    Returns:
        Corrected prices dictionary
    """
    from pricing.validation import validate_prices
    
    corrected = prices.copy()
    max_iterations = 10
    
    for _ in range(max_iterations):
       
        issues = validate_prices(corrected)
        
        if not issues:
            break
       
        structured = build_structured(corrected)
        keys_to_correct = set()
        
        # RULE 1: Product level - MTPL < Limited Casco < Casco
        
        mtpl_price = structured.get("mtpl", {}).get(None, {}).get(None)
        
        if mtpl_price is not None and "limited_casco" in structured:
            for variant in structured["limited_casco"]:
                for deductible, lc_price in structured["limited_casco"][variant].items():
                    if mtpl_price >= lc_price:
                        keys_to_correct.add("mtpl")
                        keys_to_correct.add(f"limited_casco_{variant}_{deductible}")
        

        if "limited_casco" in structured and "casco" in structured:
            for variant in VARIANT_ORDER:
                if variant not in structured["limited_casco"] or variant not in structured["casco"]:
                    continue
                
                for deductible in DEDUCTIBLE_ORDER:
                    lc_price = structured["limited_casco"][variant].get(deductible)
                    casco_price = structured["casco"][variant].get(deductible)
                    
                    if lc_price is not None and casco_price is not None:
                        if lc_price >= casco_price:
                            keys_to_correct.add(f"limited_casco_{variant}_{deductible}")
                            keys_to_correct.add(f"casco_{variant}_{deductible}")
        

        # RULE 2: Variant ordering
        
        for product in ["limited_casco", "casco"]:
            if product not in structured:
                continue
            
            for deductible in DEDUCTIBLE_ORDER:
                compact = structured[product].get("compact", {}).get(deductible)
                basic = structured[product].get("basic", {}).get(deductible)
                comfort = structured[product].get("comfort", {}).get(deductible)
                premium = structured[product].get("premium", {}).get(deductible)
                
                
                if compact is not None and comfort is not None:
                    if compact >= comfort:
                        keys_to_correct.add(f"{product}_compact_{deductible}")
                        keys_to_correct.add(f"{product}_comfort_{deductible}")
                
                
                if basic is not None and comfort is not None:
                    if basic >= comfort:
                        keys_to_correct.add(f"{product}_basic_{deductible}")
                        keys_to_correct.add(f"{product}_comfort_{deductible}")
                
                
                if comfort is not None and premium is not None:
                    if comfort >= premium:
                        keys_to_correct.add(f"{product}_comfort_{deductible}")
                        keys_to_correct.add(f"{product}_premium_{deductible}")
        
  
        # RULE 3: Deductible ordering
        
        for product in ["limited_casco", "casco"]:
            if product not in structured:
                continue
            
            for variant in VARIANT_ORDER:
                if variant not in structured[product]:
                    continue
                
                p100 = structured[product][variant].get(100)
                p200 = structured[product][variant].get(200)
                p500 = structured[product][variant].get(500)
                
               
                if p100 is not None and p200 is not None:
                    if p100 <= p200:
                        keys_to_correct.add(f"{product}_{variant}_100")
                        keys_to_correct.add(f"{product}_{variant}_200")
                
                
                if p200 is not None and p500 is not None:
                    if p200 <= p500:
                        keys_to_correct.add(f"{product}_{variant}_200")
                        keys_to_correct.add(f"{product}_{variant}_500")
        
        
        # Apply corrections - replace with reference values
        
        if not keys_to_correct:
            break
        
        for key in keys_to_correct:
            product, variant, deductible = parse_price_key(key)
            corrected[key] = calculate_reference_price(product, variant, deductible)
    
    return corrected

