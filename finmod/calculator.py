class LoanCalculator:
    @staticmethod
    def monthly_payment(amount, annual_rate_pct, months):
        if months <= 0:
            return 0.0
        r = (annual_rate_pct / 100) / 12
        pmt = 0
        if r == 0:
            pmt = ((amount / months) / 100) * 100
            return pmt
        return ((amount * r / (1 - (1 + r) ** -months)) / 100) * 100

    @staticmethod
    def outstanding_balance(amount, annual_rate_pct, months, paid_months):
        if paid_months >= months:
            return 0.0
        if paid_months <= 0:
            return amount
        r = (annual_rate_pct / 100) / 12
        if r == 0:
            return max(0, amount - (amount / months) * paid_months)
        pmt = LoanCalculator.monthly_payment(amount, annual_rate_pct, months)
        return max(0, amount * (1 + r) ** paid_months - pmt * ((1 + r) ** paid_months - 1) / r)

    @staticmethod
    def monthly_interest(balance, annual_rate_pct):
        return balance * (annual_rate_pct / 100) / 12
    
