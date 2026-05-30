# Loan Financial Model (`loanfinmod`)

A Python library for financial calculations: loan payment schedules, outstanding principal (OSP) simulations, and interest income projections. Supports both **real contract data** and **synthetic initiation scenarios**.

## Installation

### First install
```bash
pip install git+https://github.com/irsyaddamlis/loanfinmod.git
```

### Update the library
```bash
pip uninstall -y loanfinmod && pip install --no-cache-dir git+https://github.com/irsyaddamlis/loanfinmod.git
```

Make sure the version is **1.0.2**.

```python
import loanfinmod as fin
```

---

## Package Structure

```
loanfinmod/
├── calculator/
│   ├── loan_calculator.py    # Scalar math engine (LoanCalculator)
│   └── loan_dataframe.py     # DataFrame wrappers (DataFrameCalculator)
├── simulation/
│   ├── real.py               # Real contract data simulation
│   └── synthetic.py          # Synthetic initiation simulation
└── time_setup/
    └── period.py             # Time period utilities
```

---

## Function Parameters

### Payment Functions

* `df`: pandas DataFrame containing the data
* `ntf_col`: column name for loan amount
* `rate_col`: column name for annual effective rate (%)
* `tenure_col`: column name for loan tenure (months)

### Real Data Functions

* `df`: pandas DataFrame with contract data
* `agreement_col`: column name for agreement/contract ID
* `ntf_col`: column name for loan amount
* `rate_col`: column name for annual effective rate (%)
* `tenure_col`: column name for loan tenure (months)
* `golive_col`: column name for go-live date (YYYYMMDD format)
* `max_periods`: maximum projection periods (optional, defaults to max tenure)

### Initiation Functions

* `initial_booking`: initial booking amount for first period
* `growth_rate_pct`: monthly growth rate percentage
* `ticket_size`: average loan amount per agreement
* `annual_rate_pct`: annual effective rate percentage
* `tenure`: loan tenure in months
* `max_periods`: number of projection periods (if 0/None → uses tenure)

---

## Sample Data Format

Your DataFrame should contain the following columns:  
*Column names are dynamic and follow the column names in your dataframe.*

| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| Agreement Column | string/numeric | Unique contract/agreement ID | 'AGR001', 1234566789 |
| NTF Amount Column | numeric | NTF amount (loan principal) | 10000000, 15000000 |
| Rate Column | numeric | Annual effective rate (percentage) | 36.0, 42.5 |
| Tenure Column | integer | Loan tenure in months | 6, 12, 18, 24 |
| GoLive Date Column | string/numeric | Contract start date (YYYYMMDD format) | 20250102, 20250115 |

### Sample Data Example

```python
import pandas as pd

sample_data = pd.DataFrame({
    'AgreementNo': ['AGR001', 'AGR002', 'AGR003', 'AGR004', 'AGR005'],
    'Booking_NTF_Amount': [10000000, 15000000, 8000000, 12000000, 5000000],
    'Effective_Rate': [36.0, 42.5, 38.2, 40.1, 45.8],
    'Tenor': [6, 12, 9, 18, 24],
    'SK_GoLive_Date': [20250102, 20250115, 20241201, 20250101, 20250110]
})
```

**Important Notes:**
- Column names can be customized — match them with function parameters
- GoLive date must be in YYYYMMDD format
- Effective rate should be in percentage (36.0 = 36% per year)
- All numeric values must be valid (no null values for required columns)

---

## Public Functions

### 1. Scalar Calculator Functions

These operate on individual scalar values and can be used directly without a DataFrame.

```python
# Calculate PMT (periodic payment)
pmt_value = fin.pmt(ntf=10000000, annual_rate_pct=36.0, tenure=12)

# Calculate rounded installment amount
installment_value = fin.installment(ntf=10000000, annual_rate_pct=36.0, tenure=12)

# Calculate principal payment for a period
principal = fin.principal_payment(pmt=pmt_value, osp_last_month=9000000, annual_rate_pct=36.0)

# Calculate current outstanding principal
current_osp = fin.osp(osp_last_month=9000000, principal_payment=principal)

# Calculate interest income for a period
interest = fin.interest_income(installment=installment_value, principal_payment=principal)
```

---

### 2. DataFrame Payment Functions

#### a. Calculate PMT

```python
# Add a new column to DataFrame
sample_data['pmt'] = fin.calculate_pmt(
    df=sample_data,
    ntf_col="Booking_NTF_Amount",
    rate_col="Effective_Rate",
    tenure_col="Tenor"
)

# Return values only
pmt_values = fin.calculate_pmt(
    df=sample_data,
    ntf_col="Booking_NTF_Amount",
    rate_col="Effective_Rate",
    tenure_col="Tenor"
)
```

#### b. Calculate Installment

```python
# Add a new column to DataFrame
sample_data['installment'] = fin.calculate_installment(
    df=sample_data,
    ntf_col="Booking_NTF_Amount",
    rate_col="Effective_Rate",
    tenure_col="Tenor"
)

# Return values only
installment_values = fin.calculate_installment(
    df=sample_data,
    ntf_col="Booking_NTF_Amount",
    rate_col="Effective_Rate",
    tenure_col="Tenor"
)
```

---

### 3. Simulation – Real Data

This is used if we want to simulate the outstanding principal and interest income from the date of a new loan booking through the entire tenure of all contracts

#### a. Calculate Outstanding Principal (OSP)

```python
osp = fin.calculate_osp(
    df=sample_data,
    agreement_col="AgreementNo",
    ntf_col="Booking_NTF_Amount",
    tenure_col="Tenor",
    rate_col="Effective_Rate",
    golive_col="SK_GoLive_Date",
    max_periods=12  # Optional: if not provided, uses max tenure
)
```

#### b. Calculate Interest Income

```python
income = fin.calculate_income(
    df=sample_data,
    agreement_col="AgreementNo",
    ntf_col="Booking_NTF_Amount",
    tenure_col="Tenor",
    rate_col="Effective_Rate",
    golive_col="SK_GoLive_Date",
    max_periods=12  # Optional: if not provided, uses max tenure
)
```

---

### 4. Simulation – Initiation

`fin.initiation` is used to predict future loan bookings by referencing the projected growth rate which requires the initial loan booking as a baseline

#### a. Calculate OSP

```python
init_osp = fin.initiation.calculate_osp(
    initial_booking=5000000000,
    growth_rate_pct=10,
    ticket_size=100000000,
    annual_rate_pct=24,
    tenure=18,
    # max_periods=12  # Optional: if not provided, uses tenure
)
```

#### b. Calculate Interest Income

```python
init_income = fin.initiation.calculate_income(
    initial_booking=5000000000,
    growth_rate_pct=10,
    ticket_size=100000000,
    annual_rate_pct=24,
    tenure=18,
    # max_periods=12  # Optional: if not provided, uses tenure
)
```

---


