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
│   ├── __init__.py           # Package initialization
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
- Python 3.8 or higher
- pytest (for running tests)

### Setup

```bash
# Navigate to project directory
cd pricing-validation

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
    "casco_basic_100": 800,  # ❌ Violation: should be > Limited Casco
}

# Step 1: Validate
issues = validate_prices(prices)
if issues:
    print("❌ Found pricing violations:")
    for issue in issues:
        print(f"  • {issue}")

# Step 2: Auto-correct
corrected = correct_prices(prices)

# Step 3: Verify correction
remaining_issues = validate_prices(corrected)
if not remaining_issues:
    print("✅ All violations fixed!")
```

### Example Output

```
1. Validating original prices...
   Found 11 issue(s):
   1. Limited Casco compact_100 (820) must be lower than Casco compact_100 (750)
   2. Limited Casco basic_100 (900) must be lower than Casco basic_100 (830)
   ...

2. Applying automatic corrections...

3. Validating corrected prices...
   All issues resolved!

4. Price changes:
   limited_casco_compact_100: 820.00 → 700.00
   casco_compact_100: 750.00 → 900.00
   ...
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

### Check Test Coverage

```bash
pip install pytest-cov
pytest --cov=pricing --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

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

| Variant | Multiplier |    Calculation     |
|---------|------------|--------------------|
| Compact | 1.00       | Base × 1.00        |
| Basic   | 1.00       | Base × 1.00        |
| Comfort | 1.07       | Base × 1.07 (+7%)  |
| Premium | 1.14       | Base × 1.14 (+14%) |

### Deductible Adjustments

| Deductible | Multiplier |     Calculation       |
|------------|------------|-----------------------|
| 100€       | 1.00       | Variant × 1.00        |
| 200€       | 0.90       | Variant × 0.90 (-10%) |
| 500€       | 0.80       | Variant × 0.80 (-20%) |

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

|             Key             |    Calculation   | Result  |
|-----------------------------|------------------|---------|
| `mtpl`                      | 400              | 400.00€ |
| `limited_casco_basic_100`   | 700 × 1.0 × 1.0  | 700.00€ |
| `limited_casco_comfort_100` | 700 × 1.07 × 1.0 | 749.00€ |
| `limited_casco_premium_200` | 700 × 1.14 × 0.9 | 718.20€ |
| `casco_basic_500`           | 900 × 1.0 × 0.8  | 720.00€ |
| `casco_comfort_200`         | 900 × 1.07 × 0.9 | 866.70€ |
| `casco_premium_500`         | 900 × 1.14 × 0.8 | 820.80€ |

---

## 🎨 Design Decisions

### 1. Simplicity First

**Philosophy:** Clear, maintainable code over clever abstractions.

- Pure Python (no external dependencies except pytest)
- Straightforward logic flow
- Explicit rather than implicit

### 2. Separation of Concerns

**Structure:**
- `parsing.py` - Handles key format parsing
- `validation.py` - Detects rule violations
- `correction.py` - Fixes violations
- `rules.py` - Centralizes business constants

### 3. Validation Strategy

**Returns issues list instead of throwing exceptions:**
```python
issues = validate_prices(prices)  # Returns List[str]
if issues:
    # Handle violations
```

**Benefits:**
- Check all rules at once (not just first failure)
- Non-intrusive (doesn't interrupt flow)
- Easy to display multiple violations to users

### 4. Correction Strategy

**Approach:** Replace violated prices with mathematically consistent reference values.

**Why this approach?**
- **Predictable:** Same input always produces same output
- **Consistent:** All prices follow exact same formula
- **Simple:** No complex logic to maintain
- **Aligned with spec:** Task explicitly says "using the following reference values"

**Alternative considered:** Minimal adjustments to preserve original prices.
**Decision:** Reference replacement chosen for simplicity and predictability.

### 5. Testing Strategy

**Three-layer coverage:**
1. **Unit tests** - Individual functions (parsing, calculations)
2. **Integration tests** - End-to-end validation + correction
3. **Edge cases** - Empty data, partial data, extreme values

**Test philosophy:** Both positive (valid inputs) and negative (violations) cases.

---

## 🔍 Key Features

✅ **Type Safety** - Full type hints throughout codebase  
✅ **Well Documented** - Clear docstrings for all functions  
✅ **Comprehensive Tests** - 20+ unit tests covering all scenarios  
✅ **Zero Dependencies** - Pure Python (only pytest for testing)  
✅ **Business Aligned** - Code reflects real insurance pricing logic  
✅ **Maintainable** - Clear structure, meaningful names, simple logic  

---

## 📈 Future Enhancements

Potential improvements (not implemented to maintain simplicity):

- [ ] Configuration file for reference prices (YAML/JSON)
- [ ] Multiple correction strategies (conservative vs. aggressive)
- [ ] Price history tracking and audit trail
- [ ] Support for additional products (Travel, Home insurance)
- [ ] API endpoint for validation/correction
- [ ] Database integration for persistent pricing

---

## 🤝 Contributing

This is a technical assignment submission. Not accepting external contributions.

---

## 📄 License

Internal use only - Ominimo Technical Assignment

---

## 👤 Author

**Katarina**  
Technical Assignment for Ominimo  
Date: December 2024
