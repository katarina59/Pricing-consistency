from typing import Dict
from pricing.rules import (
    VARIANT_ORDER,
    DEDUCTIBLE_ORDER,
    VARIANT_STEP_PERCENT,
    MTPL_TO_LIMITED_CASCO_MARGIN,
    LIMITED_CASCO_TO_CASCO_MARGIN,
)


# Corrects pricing violations by ensuring all hierarchy rules and ordering constraints are satisfied
# Applies corrections in sequence: MTPL < Limited Casco < Casco, then enforces deductible (100 > 200 > 500) and variant (Compact/Basic < Comfort < Premium) ordering
def correct_prices(prices: Dict[str, float]) -> Dict[str, float]:

    corrected = prices.copy()

    # Step 1: Correct Limited Casco
    # First ensure all Limited Casco prices are > MTPL
    mtpl_price = corrected.get("mtpl")
    if mtpl_price is not None:
        for variant in VARIANT_ORDER:
            for deductible in DEDUCTIBLE_ORDER:
                key = f"limited_casco_{variant}_{deductible}"
                if key in corrected and corrected[key] <= mtpl_price:
                    corrected[key] = mtpl_price * (1 + MTPL_TO_LIMITED_CASCO_MARGIN)

    # Correct Limited Casco deductible ordering (100 > 200 > 500)
    for variant in VARIANT_ORDER:
        for _ in range(3): 
            changed = False
            p100_key = f"limited_casco_{variant}_100"
            p200_key = f"limited_casco_{variant}_200"
            p500_key = f"limited_casco_{variant}_500"

            p100 = corrected.get(p100_key)
            p200 = corrected.get(p200_key)
            p500 = corrected.get(p500_key)

            # Enforce 100 > 200
            if p100 is not None and p200 is not None:
                if p100 <= p200:
                    corrected[p100_key] = p200 * 1.10
                    changed = True

            # Enforce 200 > 500
            if p200 is not None and p500 is not None:
                if p200 <= p500:
                    corrected[p200_key] = p500 * 1.10
                    changed = True

            if not changed:
                break

    # Correct Limited Casco variant ordering (Compact/Basic < Comfort < Premium)
    for deductible in DEDUCTIBLE_ORDER:
        compact_key = f"limited_casco_compact_{deductible}"
        basic_key = f"limited_casco_basic_{deductible}"
        comfort_key = f"limited_casco_comfort_{deductible}"
        premium_key = f"limited_casco_premium_{deductible}"

        compact = corrected.get(compact_key)
        basic = corrected.get(basic_key)
        comfort = corrected.get(comfort_key)
        premium = corrected.get(premium_key)

        baseline = compact if compact is not None else basic

        # Enforce Comfort > baseline
        if comfort is not None and baseline is not None:
            if comfort <= baseline:
                corrected[comfort_key] = baseline * (1 + VARIANT_STEP_PERCENT)

        # Enforce Premium > Comfort
        if premium is not None and comfort is not None:
            comfort = corrected[comfort_key]  # Re-read in case it was updated
            if premium <= comfort:
                corrected[premium_key] = comfort * (1 + VARIANT_STEP_PERCENT)

    # Step 2: Correct Casco
    # First ensure all Casco prices are > Limited Casco (for same variant/deductible)
    for variant in VARIANT_ORDER:
        for deductible in DEDUCTIBLE_ORDER:
            lc_key = f"limited_casco_{variant}_{deductible}"
            c_key = f"casco_{variant}_{deductible}"

            if lc_key in corrected and c_key in corrected:
                if corrected[c_key] <= corrected[lc_key]:
                    corrected[c_key] = corrected[lc_key] * (1 + LIMITED_CASCO_TO_CASCO_MARGIN)

    # Correct Casco deductible ordering (100 > 200 > 500)
    for variant in VARIANT_ORDER:
        for _ in range(3):  
            changed = False
            p100_key = f"casco_{variant}_100"
            p200_key = f"casco_{variant}_200"
            p500_key = f"casco_{variant}_500"

            p100 = corrected.get(p100_key)
            p200 = corrected.get(p200_key)
            p500 = corrected.get(p500_key)

            # Enforce 100 > 200
            if p100 is not None and p200 is not None:
                if p100 <= p200:
                    corrected[p100_key] = p200 * 1.10
                    changed = True

            # Enforce 200 > 500
            if p200 is not None and p500 is not None:
                if p200 <= p500:
                    corrected[p200_key] = p500 * 1.10
                    changed = True

            if not changed:
                break

    # Correct Casco variant ordering (Compact/Basic < Comfort < Premium)
    for deductible in DEDUCTIBLE_ORDER:
        compact_key = f"casco_compact_{deductible}"
        basic_key = f"casco_basic_{deductible}"
        comfort_key = f"casco_comfort_{deductible}"
        premium_key = f"casco_premium_{deductible}"

        compact = corrected.get(compact_key)
        basic = corrected.get(basic_key)
        comfort = corrected.get(comfort_key)
        premium = corrected.get(premium_key)

        baseline = compact if compact is not None else basic

        # Enforce Comfort > baseline
        if comfort is not None and baseline is not None:
            if comfort <= baseline:
                corrected[comfort_key] = baseline * (1 + VARIANT_STEP_PERCENT)

        # Enforce Premium > Comfort
        if premium is not None and comfort is not None:
            comfort = corrected[comfort_key]  # Re-read in case it was updated
            if premium <= comfort:
                corrected[premium_key] = comfort * (1 + VARIANT_STEP_PERCENT)

    return corrected
