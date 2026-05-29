from __future__ import annotations

from typing import Optional

import pandas as pd

from ..calculator import LoanCalculator
from ..time_setup import build_month_labels


class Real:
    @staticmethod
    def calculate_osp(df, agreement_col, ntf_col, rate_col, tenure_col, golive_col, max_periods: Optional[int] = None, calc=None):
        """
        Calculate Outstanding Principal (OSP) for real loan data.
    
        Args:
            df: Input DataFrame containing loan data
            agreement_col: Column name for agreement IDs
            ntf_col: Column name for loan amount (NTF)
            rate_col: Column name for annual interest rate
            tenure_col: Column name for loan tenure (months)
            golive_col: Column name for go-live date (format: YYYYMMDD)
            max_periods: Maximum projection periods (auto-calculated if None)
            calc: Optional LoanCalculator instance (creates new one if None)
    
        Returns:
            DataFrame with OSP columns per period (OSP_YYYY-MM)
        """
        calculator = calc if calc else LoanCalculator()
        data = df.copy()
        if not max_periods:
            min_golive = pd.to_datetime(data[golive_col].min(), format="%Y%m%d")
            golive_dates = pd.to_datetime(data[golive_col], format="%Y%m%d")

            months_from_start = ((golive_dates.dt.year - min_golive.year) * 12 +
                                (golive_dates.dt.month - min_golive.month))

            contract_end_periods = months_from_start + data[tenure_col]

            max_periods = contract_end_periods.max() + 1
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
            )
        
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
        
        return result_df

    @staticmethod
    def calculate_income(df, agreement_col, ntf_col, rate_col, tenure_col, golive_col, max_periods: Optional[int] = None, calc=None):
        """
        Calculate interest income for real loan data.

        Args:
            df: Input DataFrame containing loan data
            agreement_col: Column name for agreement IDs
            ntf_col: Column name for loan amount (NTF)
            rate_col: Column name for annual interest rate
            tenure_col: Column name for loan tenure (months)
            golive_col: Column name for go-live date (format: YYYYMMDD)
            max_periods: Maximum projection periods (auto-calculated if None)
            calc: Optional LoanCalculator instance (creates new one if None)

        Returns:
            DataFrame with income columns per period (Income_YYYY-MM)
        """
        calculator = calc if calc else LoanCalculator()
        data = df.copy()

        data = df.copy()
        if not max_periods:
            # Calculate optimal max_periods based on actual contract end periods
            min_golive = pd.to_datetime(data[golive_col].min(), format="%Y%m%d")
            golive_dates = pd.to_datetime(data[golive_col], format="%Y%m%d")

            # Calculate months from min_golive to each contract's golive date
            months_from_start = ((golive_dates.dt.year - min_golive.year) * 12 +
                                (golive_dates.dt.month - min_golive.month))

            # Add each contract's tenure to get their end period
            contract_end_periods = months_from_start + data[tenure_col]

            # Take the maximum as our required projection length
            max_periods = contract_end_periods.max() + 1

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
            )
        
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
                
            months_elapsed = (start_dt.year - golive_date.year) * 12 + (start_dt.month - golive_date.month)
            
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