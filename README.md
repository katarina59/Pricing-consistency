# Insurance Pricing Validation & Correction System

A Python solution for validating and automatically correcting insurance product pricing according to business rules.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Business Rules](#business-rules)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Reference Pricing](#reference-pricing)
- [Examples](#examples)
- [Edge Cases & Limitations](#edge-cases--limitations)
- [Design Decisions](#design-decisions)

---

## 🎯 Overview

This system validates and corrects pricing for three motor insurance products:

|     Product       |       Description           |         Coverage Level            |
|-------------------|-----------------------------|-----------------------------------|
| **MTPL**          | Motor Third Party Liability | Basic mandatory coverage          |
| **Limited Casco** | Extended MTPL               | Covers theft and additional risks |
| **Casco**         | Full coverage               | Includes own vehicle damage       |

Each product (except MTPL) offers multiple **variants** (Compact, Basic, Comfort, Premium) and **deductible** options (100€, 200€, 500€).

---

## 📐 Business Rules

The system enforces three core pricing rules:

### 1️⃣ Product Hierarchy
```
MTPL < Limited Casco < Casco
```
Basic coverage must always be cheaper than comprehensive coverage.

### 2️⃣ Variant Ordering
```
Compact/Basic < Comfort < Premium
```
Higher tier variants cost more. **Note:** Compact and Basic relationship is flexible.

### 3️⃣ Deductible Impact
```
100€ deductible > 200€ deductible > 500€ deductible (in terms of price)
```
Higher deductibles mean lower premiums (customer assumes more risk).

---

## 📁 Project Structure

```
.
├── pricing/
│   ├── __init__.py           # Package metadata
│   ├── rules.py              # Business rules and constants
│   ├── parsing.py            # Price key parsing utilities
│   ├── validation.py         # Validation logic (detects violations)
│   └── correction.py         # Correction logic (fixes violations)
│
├── tests/
│   ├── test_parsing.py       # Tests for key parsing
│   ├── test_validation.py    # Tests for validation rules
│   └── test_correction.py    # Tests for correction logic
│
├── main.py                   # Main entry point with examples
└── README.md                 # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pytest (for running tests)

### Setup

```bash
# Navigate to project directory
cd Pricing-consistency

# Install pytest (only dependency for testing)
pip install pytest

# No other dependencies required! Pure Python solution.
```

---

## 💻 Usage

### Quick Start

Run the example from the assignment:

```bash
python3 main.py
```

This will:
1. Validate the example prices
2. Display any violations found
3. Automatically correct the violations
4. Show before/after price changes
5. Show final corrected prices

### Using in Your Code

```python
from pricing.validation import validate_prices
from pricing.correction import correct_prices

# Your insurance prices
prices = {
    "mtpl": 400,
    "limited_casco_basic_100": 850,
    "limited_casco_basic_200": 780,
    "casco_basic_100": 800,  
}

# Step 1: Validate
issues = validate_prices(prices)
if issues:
    print(" Found pricing violations:")
    for issue in issues:
        print(f"  • {issue}")

# Step 2: Auto-correct
corrected = correct_prices(prices)

# Step 3: Verify correction
remaining_issues = validate_prices(corrected)
if not remaining_issues:
    print(" All violations fixed!")

# Step 4: Show changes
changes_made = False
    for key in prices:
        if prices[key] != corrected_prices[key]:
            changes_made = True
            print(f"   {key}: {prices[key]:.2f} → {corrected_prices[key]:.2f}")
    
    if not changes_made:
        print(" No changes needed")

# Step 5: Show final
for key, value in corrected_prices.items():
        print(f"   {key}: {value:.2f}")
```

### Example Output

Real output from running `python main.py`:

```
1. Validating original prices...

 Found 11 issue(s):
   1. Limited Casco compact_100 (820) must be lower than Casco compact_100 (750)
   2. Limited Casco compact_200 (760) must be lower than Casco compact_200 (700)
   3. Limited Casco compact_500 (650) must be lower than Casco compact_500 (620)
   4. Limited Casco basic_100 (900) must be lower than Casco basic_100 (830)
   5. Limited Casco basic_200 (780) must be lower than Casco basic_200 (760)
   6. Limited Casco comfort_100 (950) must be lower than Casco comfort_100 (900)
   7. Limited Casco comfort_200 (870) must be lower than Casco comfort_200 (820)
   8. Limited Casco comfort_500 (720) must be lower than Casco comfort_500 (720)
   9. Limited Casco premium_100 (1100) must be lower than Casco premium_100 (1050)
   10. Limited Casco premium_200 (980) must be lower than Casco premium_200 (950)
   11. Limited Casco premium_500 (800) must be lower than Casco premium_500 (780)

2. Applying automatic corrections...

3. Validating corrected prices...
 All issues resolved!

4. Price changes:
   casco_compact_100: 750.00 → 918.40
   casco_compact_200: 700.00 → 851.20
   casco_compact_500: 620.00 → 728.00
   casco_basic_100: 830.00 → 1008.00
   casco_basic_200: 760.00 → 873.60
   casco_comfort_100: 900.00 → 1064.00
   casco_comfort_200: 820.00 → 974.40
   casco_comfort_500: 720.00 → 806.40
   casco_premium_100: 1050.00 → 1232.00
   casco_premium_200: 950.00 → 1097.60
   casco_premium_500: 780.00 → 896.00

5. Final corrected prices:
   mtpl: 400.00
   limited_casco_compact_100: 820.00
   limited_casco_compact_200: 760.00
   limited_casco_compact_500: 650.00
   limited_casco_basic_100: 900.00
   limited_casco_basic_200: 780.00
   limited_casco_basic_500: 600.00
   limited_casco_comfort_100: 950.00
   limited_casco_comfort_200: 870.00
   limited_casco_comfort_500: 720.00
   limited_casco_premium_100: 1100.00
   limited_casco_premium_200: 980.00
   limited_casco_premium_500: 800.00
   casco_compact_100: 918.40
   casco_compact_200: 851.20
   casco_compact_500: 728.00
   casco_basic_100: 1008.00
   casco_basic_200: 873.60
   casco_basic_500: 650.00
   casco_comfort_100: 1064.00
   casco_comfort_200: 974.40
   casco_comfort_500: 806.40
   casco_premium_100: 1232.00
   casco_premium_200: 1097.60
   casco_premium_500: 896.00
```

---

## 🧪 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_validation.py
pytest tests/test_correction.py
pytest tests/test_parsing.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Test Coverage

Our test suite covers:

| Test File              | Focus Area                  | # Tests |
|------------------------|-----------------------------|---------|
| `test_parsing.py`      | Key format validation       | 5       |
| `test_validation.py`   | Rule violation detection    | 12      |
| `test_correction.py`   | Price correction logic      | 6       |

**Total: 23 test cases** ensuring 100% rule coverage across:
- Product hierarchy validation
- Variant ordering checks
- Deductible relationship validation
- Edge cases (empty data, invalid formats, extreme values)
- Correction algorithm convergence

---

## 💰 Reference Pricing

The system uses these reference values for automatic correction:

### Variant rules

```
VARIANT_ORDER = ["compact", "basic", "comfort", "premium"]
VARIANT_STEP_PERCENT = 0.07
```

### Deductible rules

```
DEDUCTIBLE_ORDER = [100, 200, 500]
DEDUCTIBLE_STEP_PERCENT = 0.10
```

### Pricing hierarchy margins

```
MTPL_TO_LIMITED_CASCO_MARGIN = 0.05  # 5% above MTPL
LIMITED_CASCO_TO_CASCO_MARGIN = 0.12  # 12% above Limited Casco
```

---

## 📊 Examples

### Example 1: Limited Casco Basic with 100€ Deductible > Casco Basic with 100€ Deductible

```python
"mtpl": 400,
"limited_casco_basic_100": 820,
"casco_basic_100": 750, 
```

### Example 2: Limited Casco Compact with 100€ Deductible > Casco Comfort with 100€ Deductible

```python
"mtpl": 400,
"limited_casco_compact_100": 800,
"limited_casco_comfort_100": 750,
```

### Example 3: Full Price List

|             Key             |        Calculation       | Result  |
|-----------------------------|--------------------------|---------|
| `mtpl`                      | 400                      | 400.00€ |
| `limited_casco_basic_500`   | 600                      | 600.00€ |
| `limited_casco_comfort_200` | 870                      | 870.00€ |
| `limited_casco_premium_500` | 800                      | 800.00€ |
| `casco_basic_500`           | 650                      | 650.00€ |   - nothing to correct 650 > 600
| `casco_comfort_200`         | 820 ≤ 870 × (1 + 0.12)   | 974.40€ |
| `casco_premium_500`         | 780 ≤ 800 × (1 + 0.12)   | 896.00€ |

---

## ⚠️ Edge Cases & Limitations

### Handled Edge Cases

✅ **Empty price dictionary** - Returns no violations  
✅ **Partial data** - Validates only existing combinations  
✅ **Missing products** - Skips validation for unavailable products  
✅ **Only MTPL** - No violations if no other products exist  
✅ **Multiple violations** - Reports all issues at once  

### Error Handling

- **Invalid key format** - Raises `ValueError` with clear message
- **Non-numeric deductible** - Raises `ValueError` during parsing
- **Unexpected key structure** - Detected and rejected immediately

### Known Limitations

⚠️ **Maximum iterations** - Correction algorithm runs max 3 iterations per constraint (with early exit if converged)
⚠️ **Equal prices** - If Limited Casco = Casco, treated as violation (must be strictly less)

### Example Edge Cases

```python
# Valid: Empty dictionary
prices = {}
issues = validate_prices(prices)  # Returns []

# Valid: Only MTPL
prices = {"mtpl": 400}
issues = validate_prices(prices)  # Returns []

# Invalid: Wrong key format
prices = {"invalid_key": 100}
# Raises ValueError: Unexpected key format

# Invalid: Non-numeric deductible
prices = {"casco_basic_abc": 100}
# Raises ValueError: Invalid deductible value
```

---

## 🎨 Design Decisions

### 1. Simplicity First

**Philosophy:** Clear, maintainable code over clever abstractions.

- Pure Python (no external dependencies except pytest)
- Straightforward logic flow
- Explicit rather than implicit
- Readable variable names and clear function purposes

### 2. Separation of Concerns

**Structure:**
- `parsing.py` - Handles key format parsing and data structuring
- `validation.py` - Detects rule violations (read-only)
- `correction.py` - Fixes violations using reference prices
- `rules.py` - Centralizes all business constants

**Benefits:**
- Easy to modify one aspect without affecting others
- Clear responsibility boundaries
- Simple to test each component independently

### 3. Validation Strategy

**Returns issues list instead of throwing exceptions:**
```python
issues = validate_prices(prices)  # Returns List[str]
if issues:
    # Handle violations
```

**Benefits:**
- Check **all rules at once** (not just first failure)
- Non-intrusive (doesn't interrupt flow)
- Easy to display multiple violations to users
- User-friendly error messages

**Alternative considered:** Raise exception on first violation  
**Decision:** List approach chosen for better user experience

### 4. Correction Strategy

**Minimal changes:** Prices that are already correct are not changed

**Business-aligned:** Price differences come from real insurance logic, not artificial formulas

**Easy to understand:** Each price change is caused by one clear rule and one fixed percentage (margin)

**Stable:** Applying the rules step by step guarantees that the prices settle into a valid structure

**Simple:** No complex logic to maintain

### 5. Testing Strategy

**Three-layer coverage:**
1. **Unit tests** - Individual functions (parsing, calculations)
2. **Integration tests** - End-to-end validation + correction flow
3. **Edge cases** - Empty data, partial data, extreme values, invalid formats

**Test philosophy:** 
- Both positive (valid inputs) and negative (violations) cases
- Test **behavior**, not implementation details
- Clear, descriptive test names

### 6. Iteration Limit & Convergence

**Problem:** Correction algorithm could theoretically loop infinitely if logic is flawed.

**Solution:** Maximum 3 iterations per ordering constraint with early exit when no changes occur.

**Why 3?**
- In practice, 1-2 iterations fix cascading ordering violations
- 3 provides reliable safety margin without over-iterating
- Early exit prevents unnecessary iterations when convergence is reached
- Still extremely fast for production use

### 7. Data Structure

**Choice:** Nested dictionary for structured representation

```python
{
    "limited_casco": {
        "basic": {100: 700, 200: 630, 500: 560},
        "comfort": {100: 749, ...}
    }
}
```

**Benefits:**
- Fast O(1) lookups
- Natural grouping by product/variant/deductible
- Easy to iterate through hierarchies

---

## 🔍 Key Features

✅ **Type Safety** - Full type hints throughout codebase  

✅ **Well Documented** - Function docstrings explain purpose and behavior

✅ **Comprehensive Tests** - 23 unit tests covering all scenarios

✅ **Zero Dependencies** - Pure Python (only pytest for testing)

✅ **Business Aligned** - Code reflects real insurance pricing logic

✅ **Maintainable** - Clear structure, meaningful names, simple logic

✅ **Error Handling** - Graceful handling of invalid inputs

✅ **Convergence Guaranteed** - Correction always produces valid pricing

---

## 📄 License

This is a technical assignment submission for Ominimo.

---

## 👤 Author

**Katarina Medić**  
Python Technical Assignment

December 2025


---





