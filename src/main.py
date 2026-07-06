from pathlib import Path
import pandas as pd

from checks import check_customers, check_materials, check_vendors
from readiness import build_summary, calculate_readiness_score

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "data" / "output"


def load_data():
    return {
        "customers": pd.read_csv(INPUT_DIR / "customers.csv", dtype=str),
        "materials": pd.read_csv(INPUT_DIR / "materials.csv", dtype=str),
        "vendors": pd.read_csv(INPUT_DIR / "vendors.csv", dtype=str),
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = load_data()

    exceptions = []
    exceptions.extend(check_customers(data["customers"]))
    exceptions.extend(check_materials(data["materials"]))
    exceptions.extend(check_vendors(data["vendors"]))

    exceptions_df = pd.DataFrame(exceptions)

    if exceptions_df.empty:
        exceptions_df = pd.DataFrame(columns=[
            "table", "row_number", "record_id", "field", "issue", "severity"
        ])

    summaries = [
        build_summary("customers", data["customers"], exceptions_df),
        build_summary("materials", data["materials"], exceptions_df),
        build_summary("vendors", data["vendors"], exceptions_df),
    ]

    summary_df = pd.DataFrame(summaries)

    total_records = sum(len(df) for df in data.values())
    overall_score = calculate_readiness_score(total_records, exceptions_df)

    summary_df.to_csv(OUTPUT_DIR / "migration_summary.csv", index=False)
    exceptions_df.to_csv(OUTPUT_DIR / "all_exceptions.csv", index=False)

    for table in data.keys():
        table_exceptions = exceptions_df[exceptions_df["table"] == table]
        table_exceptions.to_csv(OUTPUT_DIR / f"{table}_exceptions.csv", index=False)

    report = [
        "SAP Migration Readiness Report",
        "================================",
        "",
        f"Overall readiness score: {overall_score}%",
        f"Total records assessed: {total_records}",
        f"Total exceptions found: {len(exceptions_df)}",
        "",
        "Readiness by table:",
    ]

    for item in summaries:
        report.append(
            f"- {item['table']}: {item['readiness_score']}% "
            f"({item['total_exceptions']} exceptions)"
        )

    report.append("")
    report.append("Output files created in data/output/")

    (OUTPUT_DIR / "readiness_report.txt").write_text("\n".join(report))

    print("\n".join(report))


if __name__ == "__main__":
    main()
