import pandas as pd

from config import SEVERITY_POINTS


def calculate_readiness_score(total_records, exceptions_df):
    if total_records == 0:
        return 0

    if exceptions_df.empty:
        return 100

    total_penalty = exceptions_df["severity"].map(SEVERITY_POINTS).sum()
    max_possible_penalty = total_records * 10

    score = 100 - ((total_penalty / max_possible_penalty) * 100)
    return max(0, round(score, 2))


def build_summary(table_name, df, exceptions_df):
    table_exceptions = exceptions_df[exceptions_df["table"] == table_name] if not exceptions_df.empty else pd.DataFrame()

    critical_count = 0 if table_exceptions.empty else (table_exceptions["severity"] == "Critical").sum()
    high_count = 0 if table_exceptions.empty else (table_exceptions["severity"] == "High").sum()
    medium_count = 0 if table_exceptions.empty else (table_exceptions["severity"] == "Medium").sum()
    low_count = 0 if table_exceptions.empty else (table_exceptions["severity"] == "Low").sum()

    return {
        "table": table_name,
        "total_records": len(df),
        "total_exceptions": len(table_exceptions),
        "critical_errors": critical_count,
        "high_errors": high_count,
        "medium_errors": medium_count,
        "low_errors": low_count,
        "readiness_score": calculate_readiness_score(len(df), table_exceptions),
    }
