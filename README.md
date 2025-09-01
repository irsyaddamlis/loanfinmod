# Financial Model

## Synthetic
```python
from finmod.simulation import Synthetic as syn

osp_synthetic = syn.calculate_osp(
    initial_booking=10000000000,
    growth_rate_pct=10,
    ticket_size=10000000,
    annual_rate_pct=24,
    tenure=18,
    months=19
)

interest_synthetic = syn.calculate_interest(
    initial_booking=10000000000,
    growth_rate_pct=10,
    ticket_size=10000000,
    annual_rate_pct=24,
    tenure=18,
    months=19
)

print("Outstanding Principal")
display(osp_synthetic.head(5))
print("Interest Income")
display(interest_synthetic.head(5))

```

## Real Data
```python

import dataport as dp

fact_contract_sample = dp.sqlserver_query(
    query="""
        SELECT TOP (10) * FROM [DWBIBFI2_DWH].[dbo].[Fact_Contract]
        WHERE [SK_GoLive_Date] > 20250100 AND [SK_GoLive_Date] < 20250200
        UNION
        SELECT TOP (10) * FROM [DWBIBFI2_DWH].[dbo].[Fact_Contract]
        WHERE [SK_GoLive_Date] > 20250200 AND [SK_GoLive_Date] < 20250300
        UNION
        SELECT TOP (10) * FROM [DWBIBFI2_DWH].[dbo].[Fact_Contract]
        WHERE [SK_GoLive_Date] > 20250300 AND [SK_GoLive_Date] < 20250400
    """,
    server="dwhdb",
    database="DWBIBFI2_DWH",
    windows_auth=True
)

from finmod.simulation import Real as real

real_osp = real.calculate_osp(
    df=fact_contract_sample,
    agreement_col="AgreementNo",
    ntf_col="Booking_NTF_Amount",
    golive_col="SK_GoLive_Date",
    tenor_col="Tenor",
    rate_col='Effective_Rate',
    # max_periods=12 #Jika tidak diisi, akan automatis mengambil max tenure
)

real_interest = real.calculate_interest(
    df=fact_contract_sample,
    agreement_col="AgreementNo",
    ntf_col="Booking_NTF_Amount",
    golive_col="SK_GoLive_Date",
    tenor_col="Tenor",
    rate_col='Effective_Rate',
    # max_periods=12 #Jika tidak diisi, akan automatis mengambil max tenure
)

print("Outstanding Principal")
display(real_osp.head(5))
print("Interest Income")
display(real_interest.head(5))

```