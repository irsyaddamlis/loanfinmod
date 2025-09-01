from __future__ import annotations
import pandas as pd
from ..calculator import LoanCalculator

class Synthetic:
    @staticmethod
    def calculate_osp(initial_booking, growth_rate_pct, ticket_size, months, annual_rate_pct, tenure, calc=None):
        """
        Calculate OSP for synthetic simulation
        Output: loan_asset_aggregate_df
        Index waktu: 1..months (OSP_1..OSP_m)
        """
        calculator = calc if calc else LoanCalculator()
        
        agreements = []
        for start_month in range(1, months + 1):
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

            for abs_p in range(1, months + 1):
                paid = abs_p - period
                if 0 <= paid < ten:
                    os_one = calculator.outstanding_balance(ticket, rate, ten, paid)
                    os_total = os_one * n_agree
                else:
                    os_total = 0.0

                asset_row[f"OSP_{abs_p}"] = os_total

            rows_asset.append(asset_row)

        loan_asset_aggregate_df = pd.DataFrame(rows_asset).sort_values("GoLive_Period").reset_index(drop=True)
        return loan_asset_aggregate_df

    @staticmethod
    def calculate_interest(initial_booking, growth_rate_pct, ticket_size, months, annual_rate_pct, tenure, calc=None):
        """
        Calculate Interest for synthetic simulation
        Output: interest_income_aggregate_df  
        Index waktu: 1..months (Interest_1..Interest_m)
        """
        calculator = calc if calc else LoanCalculator()
        
        agreements = []
        for start_month in range(1, months + 1):
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

            for abs_p in range(1, months + 1):
                paid = abs_p - period
                if 0 <= paid < ten:
                    os_one = calculator.outstanding_balance(ticket, rate, ten, paid)
                    interest_total = calculator.monthly_interest(os_one, rate) * n_agree
                else:
                    interest_total = 0.0

                interest_row[f"Interest_{abs_p}"] = interest_total

            rows_interest.append(interest_row)

        interest_income_aggregate_df = pd.DataFrame(rows_interest).sort_values("GoLive_Period").reset_index(drop=True)
        return interest_income_aggregate_df