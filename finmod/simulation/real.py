from __future__ import annotations
import pandas as pd
from ..calculator import LoanCalculator
from ..timeline import month_between, build_month_labels, index_to_label_map
from ..validators import ensure_real_required_columns, parse_skgolivedate, ensure_defaults

class RealSimulation:
    """
    Output:
      (loan_asset_agreement_df,
       interest_income_agreement_df,
    )
    """
    def __init__(self, calc: LoanCalculator | None = None):
        self.calc = calc or LoanCalculator()

    def run(self, df: pd.DataFrame, max_periods: int | None = None):
        data = df.copy()
        ensure_real_required_columns(data)
        data = parse_skgolivedate(data)
        data = ensure_defaults(data)

        min_dt = data["SK_GoLive_Date"].min()
        data["_start_idx"] = data["SK_GoLive_Date"].apply(lambda d: month_between(min_dt, d))

        data["_ten"] = data["Tenure"].fillna(0).astype(int)
        data["_end_idx"] = data["_start_idx"] + data["_ten"].clip(lower=0) - 1
        max_end_idx = int(data["_end_idx"].max()) if len(data) else 0
        total_periods = max_periods if max_periods is not None else (max_end_idx + 1)
        total_periods = max(total_periods, 1)

        labels = build_month_labels(min_dt, total_periods)
        idx_to_label = index_to_label_map(labels)
        data["GoLive_Period"] = data["_start_idx"].map(idx_to_label)

        loan_rows, int_rows = [], []
        calc = self.calc

        for _, ag in data.iterrows():
            ag_no = ag["AgreementNo"]
            ntf = float(ag["Booking_NTF_Amount"] or 0.0)
            ten = int(ag["Tenure"] or 0)
            rate = float(ag["EffectiveRate"] or 0.0)
            prod = ag["Product"]
            start_idx = int(ag["_start_idx"])
            golive_lbl = ag["GoLive_Period"]

            pmt = calc.monthly_payment(ntf, rate, ten)
            loan_row = {
                "AgreementNo": ag_no,
                "Booking_NTF_Amount": ntf,
                "Tenure": ten,
                "EffectiveRate": rate,
                "Product": prod,
                "GoLive_Period": golive_lbl,
                "Installment": pmt,
            }
            int_row = {
                "AgreementNo": ag_no,
                "Booking_NTF_Amount": ntf,
                "Tenure": ten,
                "EffectiveRate": rate,
                "Product": prod,
                "GoLive_Period": golive_lbl,
            }

            for abs_idx in range(total_periods):
                label = idx_to_label[abs_idx]
                paid = abs_idx - start_idx
                if 0 <= paid < ten:
                    os_val = calc.outstanding_balance(ntf, rate, ten, paid)
                    in_val = calc.monthly_interest(os_val, rate)
                else:
                    os_val = 0.0
                    in_val = 0.0
                loan_row[f"OSP_{label}"] = os_val
                int_row[f"Interest_{label}"] = in_val

            loan_rows.append(loan_row)
            int_rows.append(int_row)

        loan_asset_agreement_df = pd.DataFrame(loan_rows)
        interest_income_agreement_df = pd.DataFrame(int_rows)

        return (
            loan_asset_agreement_df,
            interest_income_agreement_df,
        )
