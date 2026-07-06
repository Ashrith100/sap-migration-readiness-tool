# SAP Migration Readiness Assessment Tool

A basic Python project that simulates an SAP ECC to SAP S/4HANA migration-readiness assessment.

The tool reads synthetic SAP-style master data, checks for common migration issues, assigns severity levels, calculates readiness scores, and exports exception reports.

## What this project demonstrates

- SAP-style master data validation
- Data quality checks
- Migration readiness scoring
- Exception reporting
- Python and pandas
- Clean GitHub-ready project structure

## Tables included

- Customers
- Materials
- Vendors

## Checks performed

- Missing required fields
- Duplicate IDs
- Invalid company codes
- Invalid countries
- Invalid currencies
- Invalid email format
- Invalid material type
- Invalid unit of measure
- Invalid vendor payment terms

## Project structure

```text
sap_migration_readiness_basic/
├── data/
│   ├── input/
│   │   ├── customers.csv
│   │   ├── materials.csv
│   │   └── vendors.csv
│   └── output/
├── src/
│   ├── config.py
│   ├── checks.py
│   ├── readiness.py
│   └── main.py
├── requirements.txt
└── README.md
```

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the assessment:

```bash
python src/main.py
```

Output files will be created in:

```text
data/output/
```

## Output files

- `migration_summary.csv`
- `all_exceptions.csv`
- `customers_exceptions.csv`
- `materials_exceptions.csv`
- `vendors_exceptions.csv`
- `readiness_report.txt`

## Example resume bullet

Built a Python-based SAP migration readiness assessment tool that validated synthetic customer, vendor, and material master data using configurable business rules, generated exception reports, and calculated readiness scores for an SAP ECC to S/4HANA-style migration.
