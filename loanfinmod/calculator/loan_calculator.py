import numpy as np


class LoanCalculator:
    @staticmethod
    def pmt(ntf, annual_rate_pct, tenure) -> float:
        if tenure <= 0:
            return 0.0
        r = (annual_rate_pct / 100) / 12
        if r == 0:
            return float(ntf / tenure)
        return float(ntf * r / (1 - (1 + r) ** -tenure))

    @staticmethod
    def installment_amount(ntf, annual_rate_pct, tenure) -> float:
        if tenure <= 0:
            return 0.0
        r = (annual_rate_pct / 100) / 12
        if r == 0:
            return float((ntf / tenure) / 100 * 100)
        pmt = ntf * r / (1 - (1 + r) ** -tenure)
        return float(round(pmt / 100) * 100)

    @staticmethod
    def _principal_payment(pmt, osp_last_month, annual_rate_pct):
        monthly_rate = (annual_rate_pct / 100) / 12
        return float(pmt - (osp_last_month * monthly_rate))

    @staticmethod
    def _osp_current(osp_last_month, principal_payment):
        return float(osp_last_month - principal_payment)

    @staticmethod
    def _interest_income(installment, principal_payment):
        return float(installment - principal_payment)