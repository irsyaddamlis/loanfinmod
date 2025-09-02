# Financial Model (finmod)

A Python library for financial calculations including payment calculations, outstanding principal simulations, and interest income projections.

## Installation

```python
import finmod as fin
```

## Public Functions

The finmod library provides 6 main functions for users:

### 1. Payment Calculations

#### Calculate PMT (Payment per Month)
```python
import pandas as pd

# Sample data
df = pd.DataFrame({
    'ntf': [100000, 200000, 150000],
    'rate': [12, 15, 10], 
    'tenure': [24, 36, 12]
})

# Calculate PMT for each row
pmt_values = fin.calculate_pmt(df, 'ntf', 'rate', 'tenure')
print(pmt_values)
# Output: [4707.35, 6933.07, 13187.38]
```

#### Calculate Installment Amount (Rounded PMT)
```python
# Calculate rounded installment amounts
installment_values = fin.calculate_installment(df, 'ntf', 'rate', 'tenure')
print(installment_values)
# Output: [4700.0, 6900.0, 13200.0]
```

### 2. Real Data Simulation

#### Calculate Outstanding Principal (OSP)
```python
# Sample contract data
contract_df = pd.DataFrame({
    'agreement': ['A001', 'A002', 'A003'],
    'ntf': [100000, 200000, 150000],
    'rate': [12, 15, 10],
    'tenure': [24, 36, 12],
    'golive': [20240101, 20240115, 20240201]
})

# Calculate OSP projection
osp_result = fin.real.calculate_osp(
    df=contract_df,
    agreement_col='agreement',
    ntf_col='ntf', 
    rate_col='rate',
    tenure_col='tenure',
    golive_col='golive',
    max_periods=12  # Optional: if not provided, uses max tenure
)

print("OSP Shape:", osp_result.shape)
print("Columns:", osp_result.columns.tolist())
```

#### Calculate Interest Income
```python
# Calculate interest income projection
income_result = fin.real.calculate_income(
    df=contract_df,
    agreement_col='agreement',
    ntf_col='ntf',
    rate_col='rate', 
    tenure_col='tenure',
    golive_col='golive',
    max_periods=12  # Optional: if not provided, uses max tenure
)

print("Income Shape:", income_result.shape)
print("Columns:", income_result.columns.tolist())
```

### 3. Synthetic/Initiation Simulation

#### Calculate OSP for Synthetic Portfolio
```python
# Synthetic portfolio simulation
synthetic_osp = fin.initiation.calculate_osp(
    initial_booking=1000000,    # Initial booking amount
    growth_rate_pct=5,          # Monthly growth rate (%)
    ticket_size=50000,          # Average loan size
    max_periods=12,             # Projection periods (None = use tenure)
    annual_rate_pct=12,         # Annual interest rate (%)
    tenure=24                   # Loan tenure in months
)

print("Synthetic OSP Shape:", synthetic_osp.shape)
```

#### Calculate Interest Income for Synthetic Portfolio
```python
# Synthetic interest income simulation
synthetic_income = fin.initiation.calculate_income(
    initial_booking=1000000,    
    growth_rate_pct=5,         
    ticket_size=50000,         
    max_periods=12,            # If 0 or None, uses tenure value
    annual_rate_pct=12,        
    tenure=24                  
)

print("Synthetic Income Shape:", synthetic_income.shape)
```

## Function Parameters

### Payment Functions
- `df`: pandas DataFrame containing the data
- `ntf_col`: Column name for loan amount (Net Funded Amount)
- `rate_col`: Column name for annual interest rate (%)
- `tenure_col`: Column name for loan tenure (months)

### Real Data Functions
- `df`: pandas DataFrame with contract data
- `agreement_col`: Column name for agreement/contract ID
- `ntf_col`: Column name for loan amount
- `rate_col`: Column name for annual interest rate (%)
- `tenure_col`: Column name for loan tenure (months)
- `golive_col`: Column name for go-live date (YYYYMMDD format)
- `max_periods`: Maximum projection periods (optional, defaults to max tenure)

### Synthetic Functions
- `initial_booking`: Initial booking amount for first period
- `growth_rate_pct`: Monthly growth rate percentage
- `ticket_size`: Average loan amount per agreement
- `max_periods`: Projection periods (if 0/None, uses tenure value)
- `annual_rate_pct`: Annual interest rate percentage
- `tenure`: Loan tenure in months

## Output

- **Payment functions**: Return pandas Series with calculated values
- **OSP functions**: Return DataFrame with outstanding principal projections by period
- **Income functions**: Return DataFrame with interest income projections by period

All simulation functions include metadata columns (agreement info, booking amounts, rates, etc.) plus time-series columns for each projection period.