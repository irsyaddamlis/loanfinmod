from __future__ import annotations
import pandas as pd
from dateutil.relativedelta import relativedelta

def month_between(a: pd.Timestamp, b: pd.Timestamp) -> int:
    """Selisih bulan antar tanggal"""
    return (b.year - a.year) * 12 + (b.month - a.month)

def build_month_labels(min_dt: pd.Timestamp, total_periods: int) -> list[str]:
    "Make label Jan 25, Feb 25, ..."
    labels = []
    current = pd.Timestamp(min_dt.year, min_dt.month, 1)
    for _ in range(max(total_periods, 0)):
        labels.append(current.strftime("%b %y"))
        current = current + relativedelta(months=1)
    return labels

def index_to_label_map(labels: list[str]) -> dict[int, str]:
    return {i: lbl for i, lbl in enumerate(labels)}