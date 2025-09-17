from __future__ import annotations
import pandas as pd
from ..calculator import LoanCalculator
from ..timeline import build_month_labels, index_to_label_map
from typing import Optional
from IPython.display import display

class Real:
    @staticmethod
    def calculate_osp(df, agreement_col, ntf_col, rate_col, tenure_col, golive_col, max_periods: Optional[int] = None, calc=None):
        calculator = calc if calc else LoanCalculator()
        data = df.copy()
        if not max_periods:
            max_periods = df[tenure_col].max()

        start_date = data[golive_col].min()
        start_date = pd.to_datetime(start_date, format="%Y%m%d")
        
        if not all([ntf_col, rate_col, tenure_col]):
            raise ValueError("Missing required mapping keys")
        
        missing = [col for col in [ntf_col, rate_col, tenure_col] if col not in data.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        
        if agreement_col not in data.columns:
            data[agreement_col] = range(len(data))
        
        data[ntf_col] = data[ntf_col].astype(float)
        data[rate_col] = data[rate_col].astype(float)  
        data[tenure_col] = data[tenure_col].astype(int)
        
        
        if golive_col and golive_col in data.columns:
            data[golive_col] = pd.to_datetime(
                data[golive_col].astype(str), 
                format="%Y%m%d", 
                # errors='coerce'
            )
            # data[golive_col] = data[golive_col].fillna(pd.Timestamp(start_date))
        
        start_dt = pd.Timestamp(start_date)
        labels = build_month_labels(start_dt, max_periods)
        
        rows = []
        
        for _, row in data.iterrows():
            amount = row[ntf_col]
            rate = row[rate_col]
            tenure = row[tenure_col]
            agreement = row[agreement_col]
            
            if golive_col and golive_col in data.columns:
                golive_date = row[golive_col]
            else:
                golive_date = start_dt
                
            # Calculate months elapsed from go-live to start date
            months_elapsed = (start_dt.year - golive_date.year) * 12 + (start_dt.month - golive_date.month)
            
            # Skip agreement if already expired
            if months_elapsed >= tenure:
                continue
            
            osp_row = {
                golive_col: golive_date.strftime('%Y%m%d') if pd.notna(golive_date) else start_dt.strftime('%Y%m%d'),
                agreement_col: agreement,
                ntf_col: amount,
                tenure_col: tenure,
                rate_col: rate
            }
            
            for period in range(max_periods):
                label = labels[period]
                actual_period = months_elapsed + period
                
                if actual_period < tenure:
                    if actual_period < 0:  # Sebelum go-live
                        osp = 0.0
                    else:
                        osp = amount
                        pmt = calculator.pmt(amount, rate, tenure)
                        
                        for month in range(actual_period):
                            if osp <= 0:
                                break
                            principal_payment = calculator._principal_payment(pmt, osp, rate)
                            osp = calculator._osp_current(osp, principal_payment)
                else:
                    osp = 0.0
                
                osp_row[f'OSP_{label}'] = osp
            
            rows.append(osp_row)

        tmp = pd.DataFrame(rows)
        result_df = tmp
        
        # # Display ENR automatically as DataFrame
        # from ..calculator import LoanCalculator as LC
        # enr_values = LC.calculate_enr(result_df)
        
        # # Create ENR and ANR DataFrame
        # enr_data = {}
        # anr_data = {}
        
        # Calculate cumulative sums for ANR calculation
        # cumulative_sum = 0
        
        # for i, (col_name, value) in enumerate(enr_values.items(), 1):
        #     enr_col_name = col_name.replace('OSP_', '')
            
        #     # ENR value
        #     enr_data[enr_col_name] = value
            
        #     # ANR value (cumulative average)
        #     cumulative_sum += value
        #     anr_value = cumulative_sum / i
        #     anr_data[enr_col_name] = anr_value
        
        # # Create DataFrame with ENR and ANR rows
        # enr_anr_df = pd.DataFrame({
        #     'ENR': enr_data,
        #     'ANR': anr_data
        # }).T
        
        # print("ENR and ANR DataFrame:")
        # display(enr_anr_df)
        
        return result_df

    @staticmethod
    def calculate_income(df, agreement_col, ntf_col, rate_col, tenure_col, golive_col, max_periods: Optional[int] = None, calc=None):
        calculator = calc if calc else LoanCalculator()
        data = df.copy()
        
        data = df.copy()
        if not max_periods:
            max_periods = df[tenure_col].max()

        start_date = data[golive_col].min()
        start_date = pd.to_datetime(start_date, format="%Y%m%d")
        if not all([ntf_col, rate_col, tenure_col]):
            raise ValueError("Missing required mapping keys")
        
        missing = [col for col in [ntf_col, rate_col, tenure_col] if col not in data.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        
        if agreement_col not in data.columns:
            data[agreement_col] = range(len(data))
        
        data[ntf_col] = data[ntf_col].astype(float)
        data[rate_col] = data[rate_col].astype(float)  
        data[tenure_col] = data[tenure_col].astype(int)
        
        if golive_col and golive_col in data.columns:
            data[golive_col] = pd.to_datetime(
                data[golive_col].astype(str), 
                format="%Y%m%d", 
                # errors='coerce'
            )
            # data[golive_col] = data[golive_col].fillna(pd.Timestamp(start_date))
        
        start_dt = pd.Timestamp(start_date)
        labels = build_month_labels(start_dt, max_periods)
        
        rows = []
        
        for _, row in data.iterrows():
            amount = row[ntf_col]
            rate = row[rate_col]
            tenure = row[tenure_col]
            agreement = row[agreement_col]
            
            if golive_col and golive_col in data.columns:
                golive_date = row[golive_col]
            else:
                golive_date = start_dt
                
            # Calculate months elapsed from go-live to start date
            months_elapsed = (start_dt.year - golive_date.year) * 12 + (start_dt.month - golive_date.month)
            
            # Skip agreement if already expired
            if months_elapsed >= tenure:
                continue
            
            interest_row = {
                golive_col: golive_date.strftime('%Y%m%d') if pd.notna(golive_date) else start_dt.strftime('%Y%m%d'),
                agreement_col: agreement,
                ntf_col: amount,
                tenure_col: tenure,
                rate_col: rate
            }
            
            for period in range(max_periods):
                label = labels[period]
                actual_period = months_elapsed + period
                
                if actual_period < tenure:
                    if actual_period < 0:  # Sebelum go-live
                        interest = 0.0
                    else:
                        # Use iterative approach instead of closed form
                        osp = amount
                        pmt = calculator.pmt(amount, rate, tenure)
                        installment = calculator.installment_amount(amount, rate, tenure)
                        
                        for month in range(actual_period):
                            if osp <= 0:
                                break
                            principal_payment = calculator._principal_payment(pmt, osp, rate)
                            osp = calculator._osp_current(osp, principal_payment)
                        
                        # Interest income = installment - principal payment for current period
                        current_principal = calculator._principal_payment(pmt, osp, rate) if osp > 0 else 0
                        interest = calculator._interest_income(installment, current_principal)
                else:
                    interest = 0.0
                
                interest_row[f'Income_{label}'] = interest
            
            rows.append(interest_row)
        tmp = pd.DataFrame(rows)

        return tmp