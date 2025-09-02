import numpy as np

class LoanCalculator:
    @staticmethod
    def pmt(amount, annual_rate_pct, months) -> float:
        if months <= 0:
            return 0.0
        r = (annual_rate_pct / 100) / 12
        if r == 0:
            return amount / months
        return (amount * r / (1 - (1 + r) ** -months))

    @staticmethod
    def installment_amount(amount, annual_rate_pct, months) -> float:
        if months <= 0:
            return 0.0
        r = (annual_rate_pct / 100) / 12
        pmt = 0
        if r == 0:
            pmt = ((amount / months) / 100) * 100
            return pmt
        
        pmt = (amount * r / (1 - (1 + r) ** -months)) 
        return np.round(pmt/100, 0) * 100

    @staticmethod
    def principal_payment(pmt, osp_last_month, annual_rate_pct):
        monthly_rate = (annual_rate_pct / 100) / 12
        return pmt - (osp_last_month * monthly_rate)

    @staticmethod
    def osp_current(osp_last_month, principal_payment):
        return osp_last_month - principal_payment

    @staticmethod
    def interest_income(installment, principal_payment):
        return installment - principal_payment

    @staticmethod
    def monthly_interest(balance, annual_rate_pct):
        """
        OSPt * Rate 
        """
        return balance * (annual_rate_pct / 100) / 12
