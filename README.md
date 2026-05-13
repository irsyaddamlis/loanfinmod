# Loan Financial Model (`loanfinmod`)

A Python library for financial calculations: loan payment schedules, outstanding principal (OSP) simulations, and interest income projections. Supports both **real contract data** and **synthetic initiation scenarios**.

## Installation

### For 1st install
```bash
pip3 install git+https://github.com/irsyad.damlis/loanfinmod.git
```
### for update the library
```bash
pip3 uninstall -y loanfinmod && pip3 install --no-cache-dir git+https://github.com/irsyaddamlis/loanfinmod.git 
```

Make sure the version is **1.0.4**.

```python
import loanfinmod as fin
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

### Sample Data Example:

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
- Column names can be customized - match them with function parameters
- GoLive date must be in YYYYMMDD format
- Effective rate should be in percentage (36.0 = 36% per year)
- All numeric values must be valid (no null values for required columns)

---

## Public Functions

### 1. Payment Calculations

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
fact_contract_sample['installment'] = fin.calculate_installment(
    df=fact_contract_sample,
    ntf_col="Booking_NTF_Amount",
    rate_col="Effective_Rate",
    tenure_col="Tenor"
)

# Return values only
installment_values = fin.calculate_installment(
    df=fact_contract_sample,
    ntf_col="Booking_NTF_Amount",
    rate_col="Effective_Rate",
    tenure_col="Tenor"
)
```

---

### 2. Simulation – Real Data

#### a. Calculate Outstanding Principal (OSP)

```python
osp = fin.real.calculate_osp(
    df=fact_contract_sample,
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
income = fin.real.calculate_income(
    df=fact_contract_sample,
    agreement_col="AgreementNo",
    ntf_col="Booking_NTF_Amount",
    tenure_col="Tenor",
    rate_col="Effective_Rate",
    golive_col="SK_GoLive_Date",
    max_periods=12  # Optional: if not provided, uses max tenure
)
```

---

### 3. Simulation – Initiation

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
