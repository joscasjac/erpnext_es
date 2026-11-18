app_name = "erpnext_es"
app_title = "ERPNext Español"
app_publisher = "Quest Media Hub"
app_description = "Corrected Latin American Spanish translation of ERPNext, shipped as its own app so ERPNext stays unchanged."
app_email = "support@example.com"
app_license = "gpl-3.0"

# Install AFTER erpnext. Frappe merges every installed app's catalog in install order, so the
# entries in locale/es.po replace ERPNext's own for `es` and every `es-*` dialect.
required_apps = ["erpnext"]
