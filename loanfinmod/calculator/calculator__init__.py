from .loan_calculator import LoanCalculator
from .loan_dataframe import DataFrameCalculator

# make an alias for easier import
pmt = LoanCalculator.pmt
installment = LoanCalculator.installment_amount
principal_payment = LoanCalculator._principal_payment
osp = LoanCalculator._osp_current
interest_income = LoanCalculator._interest_income

calculate_pmt = DataFrameCalculator.calculate_pmt
calculate_installment = DataFrameCalculator.calculate_installment

__all__ = ["LoanCalculator",
           "DataFrameCalculator",
           "pmt",
           "installment",
           "principal_payment",
           "osp",
           "interest_income",
           "calculate_pmt",
           "calculate_installment"
           ]