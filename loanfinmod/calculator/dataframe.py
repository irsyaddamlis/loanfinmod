from __future__ import annotations

import pandas as pd

from .core_calculator import LoanCalculator


class DataFrameCalculator:
    """DataFrame-level wrappers around LoanCalculator scalar methods."""

    @staticmethod
    def calculate_pmt(df: pd.DataFrame, ntf_col: str, rate_col: str, tenure_col: str) -> pd.Series:
        """
        Calculate PMT for each row in a DataFrame.

        Args:
            df: Input DataFrame
            ntf_col: Column name for loan principal amount
            rate_col: Column name for annual interest rate
            tenure_col: Column name for loan tenure in months

        Returns:
            Series of PMT values
        """
        return df.apply(
            lambda row: LoanCalculator.pmt(row[ntf_col], row[rate_col], row[tenure_col]),
            axis=1
        )

    @staticmethod
    def calculate_installment(df: pd.DataFrame, ntf_col: str, rate_col: str, tenure_col: str) -> pd.Series:
        """
        Calculate rounded installment amount for each row in a DataFrame.

        Args:
            df: Input DataFrame
            ntf_col: Column name for loan principal amount
            rate_col: Column name for annual interest rate
            tenure_col: Column name for loan tenure in months

        Returns:
            Series of installment amounts
        """
        return df.apply(
            lambda row: LoanCalculator.installment_amount(row[ntf_col], row[rate_col], row[tenure_col]),
            axis=1
        )
