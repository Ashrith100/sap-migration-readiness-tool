VALID_COMPANY_CODES = {"1000", "2000", "3000"}
VALID_COUNTRIES = {"US", "CA", "MX", "IN", "GB"}
VALID_CURRENCIES = {"USD", "CAD", "MXN", "INR", "GBP"}

VALID_MATERIAL_TYPES = {"FERT", "HALB", "ROH", "DIEN"}
VALID_UNITS_OF_MEASURE = {"EA", "KG", "LB", "L", "M"}

VALID_PAYMENT_TERMS = {"NET30", "NET45", "NET60", "DUE_ON_RECEIPT"}

REQUIRED_FIELDS = {
    "customers": ["customer_id", "customer_name", "company_code", "country", "currency"],
    "materials": ["material_id", "material_description", "material_type", "base_uom"],
    "vendors": ["vendor_id", "vendor_name", "company_code", "country", "payment_terms"],
}

SEVERITY_POINTS = {
    "Critical": 10,
    "High": 6,
    "Medium": 3,
    "Low": 1,
}
