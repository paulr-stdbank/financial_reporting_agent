import pandas as pd

def calc_ratios(df: pd.DataFrame) -> pd.DataFrame:
    ratios = df.copy()
    ratios["gross_margin"]  = df["grossProfit"] / df["revenue"]
    ratios["oper_margin"]   = df["operatingIncome"] / df["revenue"]
    ratios["net_margin"]    = df["netIncome"] / df["revenue"]
    ratios["debt_equity"]   = df["totalDebt"] / df["totalEquity"]
    ratios["return_on_eq"]  = df["netIncome"] / df["totalEquity"]
    return ratios.round(3)

def yoy_growth(df: pd.DataFrame, col: str) -> pd.Series:
    return df[col].pct_change().round(3)
