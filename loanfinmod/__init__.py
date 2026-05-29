from importlib.metadata import version

from .calculator import (calculate_installment, calculate_pmt, installment,
                         interest_income, osp, pmt, principal_payment)
from .simulation import initiation, real

__version__ = version("loanfinmod")
__author__ = "Irsyad Damlis"
__email__ = "irsyad.damlis@gmail.com"
__license__ = "MIT"

# Make an alias for easier import
calculate_osp = real.calculate_osp
calculate_income = real.calculate_income

__all__ = [
    "pmt",
    "installment",
    "principal_payment",
    "osp",
    "interest_income",
    "calculate_pmt",
    "calculate_installment",
    "calculate_osp",
    "calculate_income",
    "initiation"
]
