from __future__ import annotations
import pandas as pd
from ..calculator import LoanCalculator
from typing import Optional

class Synthetic:
    @staticmethod
    def calculate_osp(initial_booking: float, growth_rate_pct: float, ticket_size: float, annual_rate_pct: float, tenure: int, max_periods: Optional[int]=None, calc=None):
        """
        Calculate OSP for synthetic simulation
        Output: loan_asset_aggregate_df
        Index waktu: 1..max_periods (OSP_1..OSP_m)
        """
        calculator = calc if calc else LoanCalculator()
        
        # Use max tenure if max_periods is 0 or None
        if not max_periods or max_periods <= 0:
            max_periods = tenure
        
        agreements = []
        for start_month in range(1, max_periods + 1):
            booking_amount = initial_booking * ((1 + growth_rate_pct / 100) ** (start_month - 1))
            if ticket_size <= 0:
                continue
            n_agree = int(round(booking_amount / ticket_size))
            if n_agree <= 0:
                continue
            agreements.append({
                "GoLive_Period": start_month,
                "n_agree": n_agree,
                "ticket_size": ticket_size,
                "rate": annual_rate_pct,
                "tenure": tenure
            })

        rows_asset = []
        for row in agreements:
            period = row["GoLive_Period"]
            n_agree = row["n_agree"]
            ticket = row["ticket_size"]
            rate = row["rate"]
            ten = row["tenure"]

            asset_row = {"GoLive_Period": period, "SalesBooking": n_agree * ticket}

            for abs_p in range(1, max_periods + 1):
                paid = abs_p - period
                if 0 <= paid < ten:
                    # Use iterative approach instead of closed form
                    osp = ticket
                    pmt = calculator.pmt(ticket, rate, ten)
                    
                    for month in range(paid):
                        if osp <= 0:
                            break
                        principal_payment = calculator._principal_payment(pmt, osp, rate)
                        osp = calculator._osp_current(osp, principal_payment)
                    
                    os_total = osp * n_agree
                else:
                    os_total = 0.0

                asset_row[f"OSP_{abs_p}"] = os_total

            rows_asset.append(asset_row)

        loan_asset_aggregate_df = pd.DataFrame(rows_asset).sort_values("GoLive_Period").reset_index(drop=True)
        return loan_asset_aggregate_df

    @staticmethod
    def calculate_income(initial_booking: float, growth_rate_pct: float, ticket_size: float,  annual_rate_pct: float, tenure: int, max_periods: Optional[int]=None, calc=None):
        """
        Calculate Interest for synthetic simulation
        Output: interest_income_aggregate_df  
        Index waktu: 1..max_periods (Interest_1..Interest_m)
        """
        calculator = calc if calc else LoanCalculator()
        
        # Use max tenure if max_periods is 0 or None
        if not max_periods or max_periods <= 0:
            max_periods = tenure
        
        agreements = []
        for start_month in range(1, max_periods + 1):
            booking_amount = initial_booking * ((1 + growth_rate_pct / 100) ** (start_month - 1))
            if ticket_size <= 0:
                continue
            n_agree = int(round(booking_amount / ticket_size))
            if n_agree <= 0:
                continue
            agreements.append({
                "GoLive_Period": start_month,
                "n_agree": n_agree,
                "ticket_size": ticket_size,
                "rate": annual_rate_pct,
                "tenure": tenure
            })

        rows_interest = []
        for row in agreements:
            period = row["GoLive_Period"]
            n_agree = row["n_agree"]
            ticket = row["ticket_size"]
            rate = row["rate"]
            ten = row["tenure"]

            interest_row = {"GoLive_Period": period}

            for abs_p in range(1, max_periods + 1):
                paid = abs_p - period
                if 0 <= paid < ten:
                    # Use iterative approach instead of closed form
                    osp = ticket
                    pmt = calculator.pmt(ticket, rate, ten)
                    installment = calculator.installment_amount(ticket, rate, ten)
                    
                    for month in range(paid):
                        if osp <= 0:
                            break
                        principal_payment = calculator._principal_payment(pmt, osp, rate)
                        osp = calculator._osp_current(osp, principal_payment)
                    
                    # Interest income = installment - principal payment for current period
                    current_principal = calculator._principal_payment(pmt, osp, rate) if osp > 0 else 0
                    interest_per_agreement = calculator._interest_income(installment, current_principal)
                    interest_total = interest_per_agreement * n_agree
                else:
                    interest_total = 0.0

                interest_row[f"Interest_{abs_p}"] = interest_total

            rows_interest.append(interest_row)

        interest_income_aggregate_df = pd.DataFrame(rows_interest).sort_values("GoLive_Period").reset_index(drop=True)
        return interest_income_aggregate_df