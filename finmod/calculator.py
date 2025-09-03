import numpy as np

class LoanCalculator:
    @staticmethod
    def pmt(ntf, annual_rate_pct, tenure) -> float:
        if tenure <= 0:
            return 0.0
        r = (annual_rate_pct / 100) / 12
        if r == 0:
            return ntf / tenure
        return (ntf * r / (1 - (1 + r) ** -tenure))

    @staticmethod
    def installment_amount(ntf, annual_rate_pct, tenure) -> float:
        if tenure <= 0:
            return 0.0
        r = (annual_rate_pct / 100) / 12
        pmt = 0
        if r == 0:
            pmt = ((ntf / tenure) / 100) * 100
            return pmt
        
        pmt = (ntf * r / (1 - (1 + r) ** -tenure)) 
        return np.round(pmt/100, 0) * 100

    @staticmethod
    def _principal_payment(pmt, osp_last_month, annual_rate_pct):
        monthly_rate = (annual_rate_pct / 100) / 12
        return pmt - (osp_last_month * monthly_rate)

    @staticmethod
    def _osp_current(osp_last_month, principal_payment):
        return osp_last_month - principal_payment

    @staticmethod
    def _interest_income(installment, principal_payment):
        return installment - principal_payment
