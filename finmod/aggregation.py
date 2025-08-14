# aggregation.py
from __future__ import annotations
import pandas as pd

def aggregate_by_golive_period(df_in: pd.DataFrame, labels: list[str]) -> pd.DataFrame:
    """Agregasi numerik per GoLive_Period & sort berdasarkan urutan label."""
    if "GoLive_Period" not in df_in.columns:
        raise ValueError("GoLive_Period is missing for aggregation.")
    num_cols = df_in.select_dtypes(include=["number"]).columns.tolist()
    keep = ["GoLive_Period"] + [c for c in num_cols if c != "GoLive_Period"]
    out = df_in[keep].groupby("GoLive_Period", as_index=False).sum()
    cat = pd.Categorical(out["GoLive_Period"], categories=labels, ordered=True)
    out = out.assign(_ord=cat).sort_values("_ord").drop(columns="_ord").reset_index(drop=True)
    return out
