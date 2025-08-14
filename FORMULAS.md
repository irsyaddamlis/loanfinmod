# Financial Modeling Formulas Documentation

This document contains all mathematical formulas implemented in the `finmod` project for loan calculations and financial simulations.

## Table of Contents
- [LoanCalculator Formulas](#loancalculator-formulas)
  - [Monthly Payment Calculation](#monthly-payment-calculation)
  - [Outstanding Balance Calculation](#outstanding-balance-calculation)
  - [Monthly Interest Calculation](#monthly-interest-calculation)
- [Simulation Formulas](#simulation-formulas)
  - [Growth Rate Calculation](#growth-rate-calculation)
  - [Number of Agreements Calculation](#number-of-agreements-calculation)

---

## LoanCalculator Formulas

The `LoanCalculator` class (`calculator.py:1`) implements standard annuity-based loan calculation formulas.

### Monthly Payment Calculation

**Location:** `calculator.py:5-11`

**Formula:**
```
PMT = P × r / (1 - (1 + r)^(-n))
```

**Where:**
- `PMT` = Monthly payment amount
- `P` = Principal loan amount
- `r` = Monthly interest rate (annual_rate_pct / 100 / 12)
- `n` = Total number of payments (months)

**Special Cases:**
- If `r = 0` (zero interest): `PMT = P / n`
- If `n ≤ 0`: `PMT = 0`

**Implementation:**
```python
def monthly_payment(amount, annual_rate_pct, months):
    if months <= 0:
        return 0.0
    r = (annual_rate_pct / 100) / 12
    if r == 0:
        return amount / months
    return amount * r / (1 - (1 + r) ** -months)
```

### Outstanding Balance Calculation

**Location:** `calculator.py:14-23`

**Formula:**
```
OSB = P × (1 + r)^k - PMT × ((1 + r)^k - 1) / r
```

**Where:**
- `OSB` = Outstanding balance after k payments
- `P` = Original principal amount
- `r` = Monthly interest rate
- `k` = Number of payments made (paid_months)
- `PMT` = Monthly payment amount

**Special Cases:**
- If `k ≥ n` (fully paid): `OSB = 0`
- If `k ≤ 0` (no payments made): `OSB = P`
- If `r = 0` (zero interest): `OSB = max(0, P - (P/n) × k)`

**Implementation:**
```python
def outstanding_balance(amount, annual_rate_pct, months, paid_months):
    if paid_months >= months:
        return 0.0
    if paid_months <= 0:
        return amount
    r = (annual_rate_pct / 100) / 12
    if r == 0:
        return max(0, amount - (amount / months) * paid_months)
    pmt = LoanCalculator.monthly_payment(amount, annual_rate_pct, months)
    return max(0, amount * (1 + r) ** paid_months - pmt * ((1 + r) ** paid_months - 1) / r)
```

### Monthly Interest Calculation

**Location:** `calculator.py:26-27`

**Formula:**
```
Monthly Interest = Balance × (annual_rate_pct / 100) / 12
```

**Where:**
- `Balance` = Current outstanding balance
- `annual_rate_pct` = Annual interest rate as percentage

**Implementation:**
```python
def monthly_interest(balance, annual_rate_pct):
    return balance * (annual_rate_pct / 100) / 12
```

---

## Simulation Formulas

The `Simulation` class (`simulation.py:8`) implements portfolio-level calculations for loan origination modeling.

### Growth Rate Calculation

**Location:** `simulation.py:42`

**Formula:**
```
Booking Amount = Initial Booking × (1 + growth_rate_pct/100)^(start_month - 1)
```

**Where:**
- `Initial Booking` = Base booking amount for the first month
- `growth_rate_pct` = Monthly growth rate as percentage
- `start_month` = The month when booking occurs (1-indexed)

**Implementation:**
```python
booking_amount = initial_booking * ((1 + growth_rate_pct / 100) ** (start_month - 1))
```

### Number of Agreements Calculation

**Location:** `simulation.py:45`

**Formula:**
```
Number of Agreements = round(Booking Amount / Ticket Size)
```

**Where:**
- `Booking Amount` = Total booking amount for the period
- `Ticket Size` = Average loan amount per agreement

**Implementation:**
```python
n_agree = int(round(booking_amount / ticket_size))
```

### Outstanding Position Calculation (Aggregate)

**Location:** `simulation.py:78-79`

**Formula:**
```
Total Outstanding = Outstanding per Agreement × Number of Agreements
```

**Where:**
- `Outstanding per Agreement` = Result from LoanCalculator.outstanding_balance()
- `Number of Agreements` = Calculated number of loans in the cohort

**Implementation:**
```python
os_one = self.calc.outstanding_balance(ticket, rate, ten, paid)
os_total = os_one * n_agree
```

### Interest Income Calculation (Aggregate)

**Location:** `simulation.py:80`

**Formula:**
```
Total Interest = Monthly Interest per Agreement × Number of Agreements
```

**Where:**
- `Monthly Interest per Agreement` = Result from LoanCalculator.monthly_interest()
- `Number of Agreements` = Calculated number of loans in the cohort

**Implementation:**
```python
interest_total = self.calc.monthly_interest(os_one, rate) * n_agree
```

### Date Calculation Utilities

**Location:** `simulation.py:131-132`

**Formula:**
```
Months Between = (end_year - start_year) × 12 + (end_month - start_month)
```

**Where:**
- `end_year`, `end_month` = Year and month of the later date
- `start_year`, `start_month` = Year and month of the earlier date

**Implementation:**
```python
def months_between(a: pd.Timestamp, b: pd.Timestamp) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)
```

---

## Mathematical Derivations

### Monthly Payment Formula Derivation

The monthly payment formula is derived from the present value of an ordinary annuity:

```
PV = PMT × [(1 - (1 + r)^(-n)) / r]
```

Solving for PMT:
```
PMT = PV × r / (1 - (1 + r)^(-n))
```

### Outstanding Balance Formula Derivation

The outstanding balance represents the present value of remaining payments:

1. Future value of original loan after k payments: `P × (1 + r)^k`
2. Future value of payments made: `PMT × ((1 + r)^k - 1) / r`
3. Outstanding balance: `P × (1 + r)^k - PMT × ((1 + r)^k - 1) / r`

---

## Notes

- All calculations use monthly compounding
- Interest rates are assumed to be annual percentage rates
- The simulation supports both synthetic ("full") mode and real data ("real") mode
- All monetary calculations return non-negative values using `max(0, calculation)`
- Date handling uses pandas datetime functionality with relativedelta for month arithmetic