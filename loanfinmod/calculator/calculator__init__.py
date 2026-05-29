from .loan_calculator import LoanCalculator
from .loan_dataframe import DataFrameCalculator

# make an alias for easier import
pmt = staticmethod(LoanCalculator.pmt)
installment = staticmethod(LoanCalculator.installment_amount)
principal_payment = staticmethod(LoanCalculator._principal_payment)
osp = staticmethod(LoanCalculator._osp_current)
interest_income = staticmethod(LoanCalculator._interest_income)

calculate_pmt = staticmethod(DataFrameCalculator.calculate_pmt)
calculate_installment = staticmethod(DataFrameCalculator.calculate_installment)

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