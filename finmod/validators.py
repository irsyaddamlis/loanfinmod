# validators.py
from __future__ import annotations
import pandas as pd

REQUIRED_REAL_COLS = ["SK_GoLive_Date"]  # minimal wajib
DEFAULTABLE_COLS = ["AgreementNo", "Booking_NTF_Amount", "Tenure", "EffectiveRate"]

def ensure_real_required_columns(df: pd.DataFrame) -> None:
    for c in REQUIRED_REAL_COLS:
        if c not in df.columns:
            raise ValueError(f"{c} is required in real mode")

def parse_skgolivedate(df: pd.DataFrame) -> pd.DataFrame:
    """Parse SK_GoLive_Date (int/str YYYYMMDD) jadi datetime; error baris ditolak."""
    out = df.copy()
    out["SK_GoLive_Date"] = pd.to_datetime(
        out["SK_GoLive_Date"].astype(str).str.zfill(8),
        format="%Y%m%d",
        errors="coerce"
    )
    if out["SK_GoLive_Date"].isna().any():
        bad = out.index[out["SK_GoLive_Date"].isna()].tolist()
        raise ValueError(f"Found invalid SK_GoLive_Date rows: {bad}")
    return out

def ensure_defaults(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in DEFAULTABLE_COLS:
        if col not in out.columns:
            out[col] = None
    if "Product" not in out.columns:
        out["Product"] = ""
    return out
