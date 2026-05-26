from .simulation import real, synthetic
from .calculator import LoanCalculator
from importlib.metadata import version, author, email, license

__version__ = version("loanfinmod")
__author__ = author("loanfinmod")
__email__ = email("loanfinmod")
__license__ = license("loanfinmod")

# Expose main functions directly
def calculate_pmt(df, ntf_col, rate_col, tenure_col):
    """Calculate PMT for DataFrame rows"""
    def calc_pmt(row):
        return LoanCalculator.pmt(row[ntf_col], row[rate_col], row[tenure_col])
    return df.apply(calc_pmt, axis=1)

def calculate_installment(df, ntf_col, rate_col, tenure_col):
    """Calculate installment amount for DataFrame rows"""
    def calc_installment(row):
        return LoanCalculator.installment_amount(row[ntf_col], row[rate_col], row[tenure_col])
    return df.apply(calc_installment, axis=1)

initiation = synthetic

__all__ = [
    "calculate_pmt", 
    "calculate_installment", 
    "real", 
    "initiation"
]
