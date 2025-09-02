from .simulation import real, synthetic
from .calculator import LoanCalculator

# Expose main functions directly
def calculate_pmt(df, ntf_col, rate_col, tenure_col):
    def calc_pmt(row):
        return LoanCalculator.pmt(row[ntf_col], row[rate_col], row[tenure_col])
    return df.apply(calc_pmt, axis=1)

def calculate_installment(df, ntf_col, rate_col, tenure_col):
    def calc_installment(row):
        return LoanCalculator.installment_amount(row[ntf_col], row[rate_col], row[tenure_col])
    return df.apply(calc_installment, axis=1)

# Create aliases for synthetic to match your desired interface
initiation = synthetic

__all__ = ["calculate_pmt", "calculate_installment", "real", "initiation"]
