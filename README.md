# Financial Model (`finmod`)

A Python library for financial calculations: loan payment schedules, outstanding principal (OSP) simulations, and interest income projections. Supports both **real contract data** and **synthetic initiation scenarios**.

## Installation

```bash
pip uninstall -y finmod  # if already installed
pip install git+https://github.com/bfi-finance/finmod.git
```

Make sure the version is **1.0.1**.

```python
import finmod as fin
```

---

## Function Parameters

### Payment Functions

* `df`: pandas DataFrame containing the data
* `ntf_col`: column name for loan amount
* `rate_col`: column name for annual interest rate (%)
* `tenure_col`: column name for loan tenure (months)

### Real Data Functions

* `df`: pandas DataFrame with contract data
* `agreement_col`: column name for agreement/contract ID
* `ntf_col`: column name for loan amount
* `rate_col`: column name for annual interest rate (%)
* `tenure_col`: column name for loan tenure (months)
* `golive_col`: column name for go-live date (YYYYMMDD format)
* `max_periods`: maximum projection periods (optional, defaults to max tenure)

### Initiation Functions

* `initial_booking`: initial booking amount for first period
* `growth_rate_pct`: monthly growth rate percentage
* `ticket_size`: average loan amount per agreement
* `annual_rate_pct`: annual interest rate percentage
* `tenure`: loan tenure in months
* `max_periods`: number of projection periods (if 0/None → uses tenure)

---

## Public Functions

### 1. Payment Calculations

#### a. Calculate PMT

```python
# Add a new column to DataFrame
fact_contract_sample['pmt'] = fin.calculate_pmt(
    df=fact_contract_sample,
    ntf_col="Booking_NTF_Amount",
    rate_col="Effective_Rate",
    tenure_col="Tenor"
)

# Return values only
pmt_values = fin.calculate_pmt(
    df=fact_contract_sample,
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
