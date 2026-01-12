from typing import Dict, List
from pricing.parsing import build_structured
from pricing.rules import VARIANT_ORDER, DEDUCTIBLE_ORDER


# Validates pricing hierarchy and ordering constraints, returning a list of issues found
# Checks: MTPL < Limited Casco < Casco hierarchy, deductible ordering (100 > 200 > 500), and variant ordering (Compact/Basic < Comfort < Premium)
def validate_prices(prices: Dict[str, float]) -> List[str]:

    issues: List[str] = []

    structured = build_structured(prices)

    mtpl_price = structured.get("mtpl", {}).get(None, {}).get(None)

    # Check MTPL < Limited Casco hierarchy
    if mtpl_price is not None and "limited_casco" in structured:
        for variant in structured["limited_casco"]:
            for deductible, lc_price in structured["limited_casco"][variant].items():
                if mtpl_price >= lc_price:
                    issues.append(
                        f"MTPL ({mtpl_price}) must be lower than "
                        f"Limited Casco {variant}_{deductible} ({lc_price})"
                    )

    # Check Limited Casco < Casco hierarchy
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

    # Check variant ordering: Compact/Basic < Comfort < Premium
    for product in ["limited_casco", "casco"]:
        if product not in structured:
            continue

        for deductible in DEDUCTIBLE_ORDER:
            compact = structured[product].get("compact", {}).get(deductible)
            basic = structured[product].get("basic", {}).get(deductible)
            comfort = structured[product].get("comfort", {}).get(deductible)
            premium = structured[product].get("premium", {}).get(deductible)

            # Get baseline (Compact or Basic)
            baseline = compact if compact is not None else basic
            baseline_name = "compact" if compact is not None else "basic"

            # Comfort must be > baseline
            if comfort is not None and baseline is not None:
                if comfort <= baseline:
                    issues.append(
                        f"{product} {deductible}: comfort ({comfort}) "
                        f"must be higher than {baseline_name} ({baseline})"
                    )

            # Premium must be > comfort
            if comfort is not None and premium is not None:
                if premium <= comfort:
                    issues.append(
                        f"{product} {deductible}: premium ({premium}) "
                        f"must be higher than comfort ({comfort})"
                    )

    # Check deductible ordering: 100 > 200 > 500
    for product in ["limited_casco", "casco"]:
        if product not in structured:
            continue

        for variant in VARIANT_ORDER:
            if variant not in structured[product]:
                continue

            p100 = structured[product][variant].get(100)
            p200 = structured[product][variant].get(200)
            p500 = structured[product][variant].get(500)

            # 100 > 200
            if p100 is not None and p200 is not None:
                if p100 <= p200:
                    issues.append(
                        f"{product} {variant}: deductible 100 ({p100}) "
                        f"must be higher than deductible 200 ({p200})"
                    )

            # 200 > 500
            if p200 is not None and p500 is not None:
                if p200 <= p500:
                    issues.append(
                        f"{product} {variant}: deductible 200 ({p200}) "
                        f"must be higher than deductible 500 ({p500})"
                    )

    return issues