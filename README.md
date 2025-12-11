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
python main.py
```

This will:
1. Validate the example prices
2. Display any violations found
3. Automatically correct the violations
4. Show before/after price changes

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
   limited_casco_compact_100: 820.00 → 700.00
   limited_casco_compact_200: 760.00 → 630.00
   limited_casco_compact_500: 650.00 → 560.00
   limited_casco_basic_100: 900.00 → 700.00
   limited_casco_basic_200: 780.00 → 630.00
   limited_casco_basic_500: 600.00 → 560.00
   limited_casco_comfort_100: 950.00 → 749.00
   limited_casco_comfort_200: 870.00 → 674.10
   limited_casco_comfort_500: 720.00 → 599.20
   limited_casco_premium_100: 1100.00 → 798.00
   limited_casco_premium_200: 980.00 → 718.20
   limited_casco_premium_500: 800.00 → 638.40
   casco_compact_100: 750.00 → 900.00
   casco_compact_200: 700.00 → 810.00
   casco_compact_500: 620.00 → 720.00
   casco_basic_100: 830.00 → 900.00
   casco_basic_200: 760.00 → 810.00
   casco_comfort_100: 900.00 → 963.00
   casco_comfort_200: 820.00 → 866.70
   casco_comfort_500: 720.00 → 770.40
   casco_premium_100: 1050.00 → 1026.00
   casco_premium_200: 950.00 → 923.40
   casco_premium_500: 780.00 → 820.80
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
| `test_correction.py`   | Price correction logic      | 8       |

**Total: 25+ test cases** ensuring 100% rule coverage across:
- Product hierarchy validation
- Variant ordering checks
- Deductible relationship validation
- Edge cases (empty data, invalid formats, extreme values)
- Correction algorithm convergence

---

## 💰 Reference Pricing

The system uses these reference values for automatic correction:

### Base Prices

|    Product    | Base Price |
|---------------|------------|
| MTPL          | 400€       |
| Limited Casco | 700€       |
| Casco         | 900€       |

### Variant Adjustments

| Variant | Multiplier |    Calculation              | Example (700€ base) |
|---------|------------|-----------------------------|--------------------|
| Compact | 1.00       | Base × 1.00                 | 700.00€            |
| Basic   | 1.00       | Base × 1.00                 | 700.00€            |
| Comfort | 1.07       | Base × 1.07 (+7%)           | 749.00€            |
| Premium | 1.14       | Base × 1.14 (+14% = 2×7%)   | 798.00€            |

**Note:** Premium is calculated as Comfort + additional 7% (total +14% from base).

### Deductible Adjustments

| Deductible | Discount | Multiplier |     Calculation       | Example (700€ base) |
|------------|----------|------------|-----------------------|---------------------|
| 100€       | 0%       | 1.00       | Variant × 1.00        | 700.00€             |
| 200€       | -10%     | 0.90       | Variant × 0.90        | 630.00€             |
| 500€       | -20%     | 0.80       | Variant × 0.80        | 560.00€             |

### Formula

```
Final Price = Base Price × Variant Multiplier × Deductible Multiplier
```

---

## 📊 Examples

### Example 1: Limited Casco Comfort with 200€ Deductible

```python
Base: 700€ (Limited Casco)
Variant: 1.07 (Comfort = +7%)
Deductible: 0.90 (200€ = -10%)

Price = 700 × 1.07 × 0.90 = 674.10€
```

### Example 2: Casco Premium with 500€ Deductible

```python
Base: 900€ (Casco)
Variant: 1.14 (Premium = +14%)
Deductible: 0.80 (500€ = -20%)

Price = 900 × 1.14 × 0.80 = 820.80€
```

### Example 3: Full Price List

|             Key             |        Calculation       | Result  |
|-----------------------------|--------------------------|---------|
| `mtpl`                      | 400                      | 400.00€ |
| `limited_casco_basic_100`   | 700 × 1.0 × 1.0          | 700.00€ |
| `limited_casco_comfort_100` | 700 × 1.07 × 1.0         | 749.00€ |
| `limited_casco_premium_200` | 700 × 1.14 × 0.9         | 718.20€ |
| `casco_basic_500`           | 900 × 1.0 × 0.8          | 720.00€ |
| `casco_comfort_200`         | 900 × 1.07 × 0.9         | 866.70€ |
| `casco_premium_500`         | 900 × 1.14 × 0.8         | 820.80€ |

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

⚠️ **Maximum iterations** - Correction algorithm runs max 10 iterations to prevent infinite loops  
⚠️ **Equal prices** - If Limited Casco = Casco, treated as violation (must be strictly less)  
⚠️ **No partial corrections** - All violated prices replaced with reference values  
⚠️ **Key format strict** - Must follow `product_variant_deductible` pattern exactly  

### Example Edge Cases

```python
# Valid: Empty dictionary
prices = {}
issues = validate_prices(prices)  # Returns []

# Valid: Only MTPL
prices = {"mtpl": 400}
issues = validate_prices(prices)  # Returns []

# Valid: Partial product coverage
prices = {
    "mtpl": 400,
    "limited_casco_basic_100": 700
    # Casco missing - no violations
}

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

**Approach:** Replace violated prices with mathematically consistent reference values.

**Why this approach?**
- **Predictable:** Same input always produces same output
- **Consistent:** All prices follow exact same formula
- **Simple:** No complex logic to maintain
- **Aligned with spec:** Task explicitly says "using the following reference values"
- **Guaranteed convergence:** Reference prices always satisfy all rules

**Alternative considered:** Minimal adjustments to preserve original prices (e.g., increase Casco by 1€ if too low)

**Decision:** Reference replacement chosen because:
1. Original prices might be far from business model
2. Minimal adjustments could create inconsistent pricing
3. Reference values ensure complete consistency
4. Simpler to maintain and explain

### 5. Testing Strategy

**Three-layer coverage:**
1. **Unit tests** - Individual functions (parsing, calculations)
2. **Integration tests** - End-to-end validation + correction flow
3. **Edge cases** - Empty data, partial data, extreme values, invalid formats

**Test philosophy:** 
- Both positive (valid inputs) and negative (violations) cases
- Test **behavior**, not implementation details
- Use `pytest.approx()` for floating-point comparisons
- Clear, descriptive test names

### 6. Iteration Limit

**Problem:** Correction algorithm could theoretically loop infinitely if logic is flawed.

**Solution:** Maximum 10 iterations with early exit when no violations remain.

**Why 10?**
- In practice, 1-2 iterations fix all violations
- 10 provides safety margin
- Still fast enough for production use

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
✅ **Well Documented** - Clear docstrings for all functions  
✅ **Comprehensive Tests** - 25+ unit tests covering all scenarios  
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
Technical Assignment - Python Developer Position  
December 2025


---
