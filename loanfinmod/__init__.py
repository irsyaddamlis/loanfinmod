from importlib.metadata import version

from .calculator import LoanCalculator
from .simulation import real, synthetic

__version__ = version("loanfinmod")
__author__ = "Irsyad Damlis"
__email__ = "irsyad.damlis@gmail.com"
__license__ = "MIT"

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
