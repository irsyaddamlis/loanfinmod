# Financial Model

## How to use?
```python
from finmod.simulation import FullSimulation as fs
from finmod.simulation import RealSimulation as rs

## Full Simulation
"""
Input:
1. Initial Booking
2. growth_rate_pct
3. ticket_size
4. months (period to see)
5. annual_pct_rate
6. tenure
"""

loan_asset, interest_income = fs().run(
    initial_booking = 10000000000,
    growth_rate_pct = 10,
    ticket_size = 90000000,
    months = 12,
    annual_pct_rate = 24,
    tenure=18
)

## Real Simulation
filepath = "" # Input your data path
df = pd.read_excel(f"{filepath}")

loan_asset_, interest_income = rs().run(
    df_input = df,
    max_periods=12
)

```