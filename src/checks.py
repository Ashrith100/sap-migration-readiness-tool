import re
import pandas as pd

from config import (
    REQUIRED_FIELDS,
    VALID_COMPANY_CODES,
    VALID_COUNTRIES,
    VALID_CURRENCIES,
    VALID_MATERIAL_TYPES,
    VALID_UNITS_OF_MEASURE,
    VALID_PAYMENT_TERMS,
)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def add_exception(exceptions, table, row_number, record_id, field, issue, severity):
    exceptions.append({
        "table": table,
        "row_number": row_number,
        "record_id": record_id,
        "field": field,
        "issue": issue,
        "severity": severity,
    })


def check_missing_required_fields(df, table_name, id_field):
    exceptions = []
    for field in REQUIRED_FIELDS[table_name]:
        missing_rows = df[df[field].isna() | (df[field].astype(str).str.strip() == "")]
        for idx, row in missing_rows.iterrows():
            add_exception(
                exceptions,
                table_name,
                idx + 2,
                row.get(id_field, ""),
                field,
                f"Missing required field: {field}",
                "Critical",
            )
    return exceptions


def check_duplicates(df, table_name, id_field):
    exceptions = []
    duplicate_rows = df[df.duplicated(subset=[id_field], keep=False)]
    for idx, row in duplicate_rows.iterrows():
        add_exception(
            exceptions,
            table_name,
            idx + 2,
            row.get(id_field, ""),
            id_field,
            f"Duplicate {id_field}",
            "High",
        )
    return exceptions


def check_customers(df):
    exceptions = []
    table = "customers"
    id_field = "customer_id"

    exceptions.extend(check_missing_required_fields(df, table, id_field))
    exceptions.extend(check_duplicates(df, table, id_field))

    for idx, row in df.iterrows():
        record_id = row.get(id_field, "")

        if str(row.get("company_code", "")).strip() not in VALID_COMPANY_CODES:
            add_exception(exceptions, table, idx + 2, record_id, "company_code", "Invalid company code", "Critical")

        if str(row.get("country", "")).strip() not in VALID_COUNTRIES:
            add_exception(exceptions, table, idx + 2, record_id, "country", "Invalid country code", "High")

        if str(row.get("currency", "")).strip() not in VALID_CURRENCIES:
            add_exception(exceptions, table, idx + 2, record_id, "currency", "Invalid currency", "High")

        email = str(row.get("email", "")).strip()
        if email and not EMAIL_PATTERN.match(email):
            add_exception(exceptions, table, idx + 2, record_id, "email", "Invalid email format", "Medium")

    return exceptions


def check_materials(df):
    exceptions = []
    table = "materials"
    id_field = "material_id"

    exceptions.extend(check_missing_required_fields(df, table, id_field))
    exceptions.extend(check_duplicates(df, table, id_field))

    for idx, row in df.iterrows():
        record_id = row.get(id_field, "")

        if str(row.get("material_type", "")).strip() not in VALID_MATERIAL_TYPES:
            add_exception(exceptions, table, idx + 2, record_id, "material_type", "Invalid material type", "High")

        if str(row.get("base_uom", "")).strip() not in VALID_UNITS_OF_MEASURE:
            add_exception(exceptions, table, idx + 2, record_id, "base_uom", "Invalid unit of measure", "Medium")

    return exceptions


def check_vendors(df):
    exceptions = []
    table = "vendors"
    id_field = "vendor_id"

    exceptions.extend(check_missing_required_fields(df, table, id_field))
    exceptions.extend(check_duplicates(df, table, id_field))

    for idx, row in df.iterrows():
        record_id = row.get(id_field, "")

        if str(row.get("company_code", "")).strip() not in VALID_COMPANY_CODES:
            add_exception(exceptions, table, idx + 2, record_id, "company_code", "Invalid company code", "Critical")

        if str(row.get("country", "")).strip() not in VALID_COUNTRIES:
            add_exception(exceptions, table, idx + 2, record_id, "country", "Invalid country code", "High")

        if str(row.get("payment_terms", "")).strip() not in VALID_PAYMENT_TERMS:
            add_exception(exceptions, table, idx + 2, record_id, "payment_terms", "Invalid payment terms", "Medium")

    return exceptions
