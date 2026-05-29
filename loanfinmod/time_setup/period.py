from __future__ import annotations

import pandas as pd
from dateutil.relativedelta import relativedelta


class Period:
    """Utility class for time period calculations."""

    @staticmethod        
    def month_between(a: pd.Timestamp, b: pd.Timestamp) -> int:
        """Calculate number of months between two dates."""
        return (b.year - a.year) * 12 + (b.month - a.month)

    @staticmethod
    def build_month_labels(min_dt: pd.Timestamp, total_periods: int) -> list[str]:
        """
        Build a list of month labels starting from min_dt.

        Args:
            min_dt: Start date
            total_periods: Number of periods to generate

        Returns:
            List of labels in 'MMM YY' format (e.g. ['Jan 25', 'Feb 25', ...])
        """
        labels = []
        current = pd.Timestamp(min_dt.year, min_dt.month, 1)
        for _ in range(max(total_periods, 0)):
            labels.append(current.strftime("%b %y"))
            current = current + relativedelta(months=1)
        return labels

    @staticmethod
    def index_to_label_map(labels: list[str]) -> dict[int, str]:
        """Map period index to month label."""
        return {i: lbl for i, lbl in enumerate(labels)}
