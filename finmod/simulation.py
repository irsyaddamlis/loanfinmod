# simulation.py
import pandas as pd
from datetime import datetime
from .calculator import LoanCalculator
from dateutil.relativedelta import relativedelta


class Simulation:
    """
    Outputs:
      Full mode -> (loan_asset_aggregate_df, interest_income_aggregate_df)
      Real mode -> (
          loan_asset_agreement_df,
          loan_asset_aggregate_df,
          interest_income_agreement_df,
          interest_income_aggregate_df
      )
    """
    def __init__(self, mode="real"):
        if mode not in ("full", "real"):
            raise ValueError("mode must be 'full' or 'real'")
        self.mode = mode
        self.calc = LoanCalculator()

    # ================= FULL MODE ================= #
    def run_full(
        self,
        initial_booking: float,
        growth_rate_pct: float,
        ticket_size: float,
        months: int,
        annual_rate_pct: float,
        tenure: int
    ):
        """
        Full mode: hanya aggregate, dan di-index per GoLive_Period (1..months).
        Menyediakan OSP_1..OSP_{months} dan Interest_1..Interest_{months}.
        """
        # Bangun list "agreement" sintetis per bulan start (GoLive_Period = start_month)
        agreements = []
        for start_month in range(1, months + 1):
            booking_amount = initial_booking * ((1 + growth_rate_pct / 100) ** (start_month - 1))
            if ticket_size <= 0:
                continue
            n_agree = int(round(booking_amount / ticket_size))
            if n_agree <= 0:
                continue
            # catat total booking pada periode go-live tsb
            agreements.append({
                "GoLive_Period": start_month,
                "n_agree": n_agree,
                "ticket_size": ticket_size,
                "rate": annual_rate_pct,
                "tenure": tenure
            })

        # Siapkan tabel aggregate per GoLive_Period
        rows_asset = []
        rows_interest = []
        for row in agreements:
            period = row["GoLive_Period"]
            n_agree = row["n_agree"]
            ticket = row["ticket_size"]
            rate = row["rate"]
            ten = row["tenure"]

            # installment per agreement
            pmt = self.calc.monthly_payment(ticket, rate, ten)
            # base baris
            asset_row = {"GoLive_Period": period, "SalesBooking": n_agree * ticket}
            interest_row = {"GoLive_Period": period, "Installment__": n_agree * pmt}

            # absolute period 1..months
            for abs_p in range(1, months + 1):
                paid = abs_p - period  # berapa cicilan terbayar bagi cohort yang start di 'period'
                if 0 <= paid < ten:
                    # outstanding per agreement
                    os_one = self.calc.outstanding_balance(ticket, rate, ten, paid)
                    os_total = os_one * n_agree
                    interest_total = self.calc.monthly_interest(os_one, rate) * n_agree
                else:
                    os_total = 0.0
                    interest_total = 0.0

                asset_row[f"OSP_{abs_p}"] = os_total
                interest_row[f"Interest_{abs_p}"] = interest_total

            rows_asset.append(asset_row)
            rows_interest.append(interest_row)

        loan_asset_aggregate_df = pd.DataFrame(rows_asset).sort_values("GoLive_Period").reset_index(drop=True)
        interest_income_aggregate_df = pd.DataFrame(rows_interest).sort_values("GoLive_Period").reset_index(drop=True)

        return loan_asset_aggregate_df, interest_income_aggregate_df

    def run_real(self, df: pd.DataFrame, max_periods: int | None = None):
        """
        Real mode (final):
        - SK_GoLive_Date: int/str YYYYMMDD
        - GoLive_Period: label 'Jan 25', 'Feb 25', ...
        - Kolom timeline: OSP_<Label>, Interest_<Label>
        - Aggregate by GoLive_Period (label)
        """
        data = df.copy()

        # --- Parse SK_GoLive_Date (int/str YYYYMMDD) ---
        if "SK_GoLive_Date" not in data.columns:
            raise ValueError("SK_GoLive_Date is required in real mode (format YYYYMMDD, int/str).")

        # cast to string and parse strictly as YYYYMMDD
        data["SK_GoLive_Date"] = pd.to_datetime(
            data["SK_GoLive_Date"].astype(str).str.zfill(8),
            format="%Y%m%d",
            errors="coerce"
        )
        if data["SK_GoLive_Date"].isna().any():
            bad = data[data["SK_GoLive_Date"].isna()]
            raise ValueError(f"Found invalid SK_GoLive_Date rows: {bad.index.tolist()}")

        # --- Columns defaults ---
        for col in ["AgreementNo", "Booking_NTF_Amount", "Tenure", "EffectiveRate"]:
            if col not in data.columns:
                data[col] = None
        if "Product" not in data.columns:
            data["Product"] = ""

        # --- Absolute month axis ---
        min_dt = data["SK_GoLive_Date"].min()

        # helper: month diff between two dates (month starts)
        def months_between(a: pd.Timestamp, b: pd.Timestamp) -> int:
            return (b.year - a.year) * 12 + (b.month - a.month)

        # start index per agreement (0-based)
        data["_start_idx"] = data["SK_GoLive_Date"].apply(lambda d: months_between(min_dt, d))

        # total periods (if not provided): max(end_idx) + 1
        # end_idx = start_idx + Tenure - 1
        data["_ten"] = data["Tenure"].fillna(0).astype(int)
        data["_end_idx"] = data["_start_idx"] + data["_ten"].clip(lower=0) - 1
        max_end_idx = int(data["_end_idx"].max()) if len(data) else 0
        total_periods = max_periods if max_periods is not None else (max_end_idx + 1)
        total_periods = max(total_periods, 1)

        # --- Build month labels from min_dt ---
        labels = []
        current = pd.Timestamp(min_dt.year, min_dt.month, 1)
        for i in range(total_periods):
            labels.append(current.strftime("%b %y"))  # e.g., 'Jan 25'
            current = current + relativedelta(months=1)

        # map label by absolute index
        idx_to_label = {i: lbl for i, lbl in enumerate(labels)}

        # set GoLive_Period label
        data["GoLive_Period"] = data["_start_idx"].map(idx_to_label)

        # ===== Agreement-level tables =====
        calc = LoanCalculator()
        loan_rows, int_rows = [], []

        for _, ag in data.iterrows():
            ag_no = ag["AgreementNo"]
            ntf = float(ag["Booking_NTF_Amount"] or 0.0)
            ten = int(ag["Tenure"] or 0)
            rate = float(ag["EffectiveRate"] or 0.0)
            prod = ag["Product"]
            start_idx = int(ag["_start_idx"])
            golive_lbl = ag["GoLive_Period"]

            # metadata rows
            loan_row = {
                "AgreementNo": ag_no,
                "Booking_NTF_Amount": ntf,
                "Tenure": ten,
                "EffectiveRate": rate,
                "Product": prod,
                "GoLive_Period": golive_lbl
            }
            pmt = calc.monthly_payment(ntf, rate, ten)
            int_row = dict(loan_row)
            int_row["Installment"] = pmt

            # fill OSP_<Label> & Interest_<Label>
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

        # ===== Aggregate by GoLive_Period (label) =====
        def aggregate_by_glp(df_in: pd.DataFrame) -> pd.DataFrame:
            # numeric only; keep GoLive_Period for groupby
            num_cols = df_in.select_dtypes(include=["number"]).columns.tolist()
            keep = ["GoLive_Period"] + [c for c in num_cols if c != "GoLive_Period"]
            out = (
                df_in[keep]
                .groupby("GoLive_Period", as_index=False)
                .sum()
            )
            # order by chronological labels
            cat = pd.Categorical(out["GoLive_Period"], categories=labels, ordered=True)
            out = out.assign(_ord=cat).sort_values("_ord").drop(columns="_ord").reset_index(drop=True)
            return out

        loan_asset_aggregate_df = aggregate_by_glp(loan_asset_agreement_df)
        interest_income_aggregate_df = aggregate_by_glp(interest_income_agreement_df)

        # cleanup helper cols
        for c in ["_start_idx", "_ten", "_end_idx"]:
            if c in data.columns:
                data.drop(columns=c, inplace=True)

        return (
            loan_asset_agreement_df,
            loan_asset_aggregate_df,
            interest_income_agreement_df,
            interest_income_aggregate_df
        )