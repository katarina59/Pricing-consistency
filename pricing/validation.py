from typing import Dict, List, Optional
from pricing.parsing import parse_price_key
from pricing.rules import VARIANT_ORDER, DEDUCTIBLE_ORDER


def validate_prices(prices: Dict[str, float]) -> List[str]:
    """
    Validate pricing consistency according to business rules.
    
    Business rules:
    1. Product level: MTPL < Limited Casco < Casco
    2. Variant level: Compact/Basic < Comfort < Premium
    3. Deductible level: 100€ > 200€ > 500€ (higher deductible = lower price)
    
    Args:
        prices: Dictionary mapping price keys to amounts
        
    Returns:
        List of validation issues. Empty list means all rules are satisfied.
    """
    issues: List[str] = []
    
    # Restructure data for easier comparison
    # Format: structured[product][variant][deductible] = price
    structured: Dict[str, Dict[Optional[str], Dict[Optional[int], float]]] = {}

#     structured = {
#     "mtpl": {
#         None: {None: 400}
#     },
#     "limited_casco": {
#         "compact": {100: 820, 200: 760, 500: 650},
#         "basic": {100: 900, 200: 780, 500: 600},
#         # ...
#     },
#     "casco": {
#         "compact": {100: 750, 200: 700, 500: 620},
#         # ...
#     }
# }
    
    for key, price in prices.items():
        product, variant, deductible = parse_price_key(key)
        
        if product not in structured:
            structured[product] = {}
        if variant not in structured[product]:
            structured[product][variant] = {}
        
        structured[product][variant][deductible] = price

    
    # ============================================================
    # RULE 1: Product level ordering - MTPL < Limited Casco < Casco
    # ============================================================
    
    mtpl_price = structured.get("mtpl", {}).get(None, {}).get(None)
    
    # Check: MTPL must be cheaper than ALL Limited Casco variants
    if mtpl_price is not None and "limited_casco" in structured:
        for variant in structured["limited_casco"]:
            for deductible, lc_price in structured["limited_casco"][variant].items():
                if mtpl_price >= lc_price:
                    issues.append(
                        f"MTPL ({mtpl_price}) must be lower than "
                        f"Limited Casco {variant}_{deductible} ({lc_price})"
                    )
    
    # Check: Limited Casco < Casco for matching variant/deductible pairs
    if "limited_casco" in structured and "casco" in structured:
        for variant in VARIANT_ORDER:
            if variant not in structured["limited_casco"]:
                continue
            if variant not in structured["casco"]:
                continue
                
            for deductible in DEDUCTIBLE_ORDER:
                lc_price = structured["limited_casco"][variant].get(deductible)
                casco_price = structured["casco"][variant].get(deductible)
                
                if lc_price is not None and casco_price is not None:
                    if lc_price >= casco_price:
                        issues.append(
                            f"Limited Casco {variant}_{deductible} ({lc_price}) "
                            f"must be lower than Casco {variant}_{deductible} ({casco_price})"
                        )
    
    # ============================================================
    # RULE 2: Variant ordering - Compact/Basic < Comfort < Premium
    # ============================================================
    
    for product in ["limited_casco", "casco"]:
        if product not in structured:
            continue
        
        for deductible in DEDUCTIBLE_ORDER:
            # Get all variant prices for this deductible
            compact = structured[product].get("compact", {}).get(deductible)
            basic = structured[product].get("basic", {}).get(deductible)
            comfort = structured[product].get("comfort", {}).get(deductible)
            premium = structured[product].get("premium", {}).get(deductible)
            
            # Rule: Compact < Comfort
            if compact is not None and comfort is not None:
                if compact >= comfort:
                    issues.append(
                        f"{product} {deductible}: compact ({compact}) "
                        f"must be lower than comfort ({comfort})"
                    )
            
            # Rule: Basic < Comfort
            if basic is not None and comfort is not None:
                if basic >= comfort:
                    issues.append(
                        f"{product} {deductible}: basic ({basic}) "
                        f"must be lower than comfort ({comfort})"
                    )
            
            # Rule: Comfort < Premium
            if comfort is not None and premium is not None:
                if comfort >= premium:
                    issues.append(
                        f"{product} {deductible}: comfort ({comfort}) "
                        f"must be lower than premium ({premium})"
                    )
    
    # ============================================================
    # RULE 3: Deductible ordering - 100 > 200 > 500 (price-wise)
    # Higher deductible = customer pays more out of pocket = lower premium
    # ============================================================
    
    for product in ["limited_casco", "casco"]:
        if product not in structured:
            continue
        
        for variant in VARIANT_ORDER:
            if variant not in structured[product]:
                continue
            
            p100 = structured[product][variant].get(100)
            p200 = structured[product][variant].get(200)
            p500 = structured[product][variant].get(500)
            
            # Rule: 100€ deductible should be MORE expensive than 200€
            if p100 is not None and p200 is not None:
                if p100 <= p200:
                    issues.append(
                        f"{product} {variant}: deductible 100 ({p100}) "
                        f"must be higher than deductible 200 ({p200})"
                    )
            
            # Rule: 200€ deductible should be MORE expensive than 500€
            if p200 is not None and p500 is not None:
                if p200 <= p500:
                    issues.append(
                        f"{product} {variant}: deductible 200 ({p200}) "
                        f"must be higher than deductible 500 ({p500})"
                    )
    
    return issues