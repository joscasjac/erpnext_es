# Style guide and glossary

The rules every entry in `erpnext_es/locale/es.po` follows. Use them when you add or change entries.

## Style
- Neutral Latin American Spanish. No Spain-only words: coste→costo, importe→monto, compañía→empresa, ordenador→computadora, fichero→archivo, pulse→haga clic/presione, albarán→nota de entrega, TPV→PDV, pedido de venta→orden de venta, parte de horas→registro de horas.
- Informal register (tú): "Selecciona", "Ingresa", "Tu empresa", "Puedes", "para ti". Never usted ("Seleccione", "Ingrese", "Su empresa", "usted"). No vos. "su/sus" stays only when it means its/their, not your.
- Sentence case, as Spanish does: "Saldo en moneda de la cuenta", not "Saldo en Moneda de la Cuenta". Keep capitals only for the first word, proper nouns, product names (ERPNext, Frappe, Shopify, Plaid, Tally, etc.), acronyms (IVA, RFC, NIT, GST, PDV, UdM, LdM, CRM, API, URL, PDF, ID) and country/currency names.
- Button labels and menu actions stay infinitive: "Crear factura", "Validar". Field labels are noun phrases.
- Fix any mistranslation, wrong meaning, wrong gender/number agreement, missing accent, typo, doubled word, leftover English, Portuguese, or truncated text.
- Translate every untranslated entry (es is empty). Long markdown/HTML onboarding texts too, keeping the markdown/HTML structure.

## Hard rules (the tests fail otherwise)
- Keep every placeholder exactly: `{0}`, `{1}`, `{}`, `{name}`, `%s`, `%(x)s`, `{{ ... }}` Jinja. Same set, any order. If the English has `{}` keep `{}` (do not turn it into `{0}`).
- Keep every HTML tag and attribute (`<b>`, `<br>`, `<a href="...">`, classes, ids) and the same number of `\n`.
- Keep leading/trailing spaces exactly like the English (e.g. "Notes: " → "Notas: ").
- Do not translate code, field names in backticks, URLs, emails, naming-series patterns (ABCD.#####), or keys in `{}`.
- If the English is itself only a code/brand/acronym (e.g. "SWIFT", "frankfurter.dev - v2", "Incoterm code"), leave it as is.
- `ctx` (msgctxt) changes meaning: e.g. ctx "Delivery Note" vs a verb. Respect it.

## Glossary (English → Spanish). Use these exact terms, with correct article/agreement.
| English | Spanish |
|---|---|
| Item / Items | Artículo / Artículos (f.e. "Grupo de artículos", "Código de artículo", "Precio del artículo"). "Product" stays producto (Product Bundle = Paquete de productos). |
| Stock (module, quantity) | Inventario; "existencias" for on-hand quantities ("Existencias disponibles", "sin existencias"). Never "stock", never "almacén" for Stock. |
| Stock Entry | Movimiento de inventario |
| Stock Ledger / Stock Ledger Entry | Libro mayor de inventario / Registro del libro mayor de inventario |
| Stock Reconciliation | Conciliación de inventario |
| Stock Settings | Configuración de inventario |
| Warehouse | Almacén |
| Bin (doctype: item qty per warehouse) | Existencias por almacén |
| Company | Empresa |
| Customer / Supplier | Cliente / Proveedor |
| Customer Group / Supplier Group / Item Group | Grupo de clientes / Grupo de proveedores / Grupo de artículos |
| Lead | Cliente potencial (Lead Source = Origen del cliente potencial) |
| Prospect | Prospecto |
| Opportunity | Oportunidad |
| Quotation | Cotización |
| Supplier Quotation | Cotización de proveedor |
| Request for Quotation | Solicitud de cotización |
| Budget | Presupuesto (only for Budget!) |
| Sales Order / Purchase Order | Orden de venta / Orden de compra (no "(OV)"/"(OC)", no "pedido") |
| Delivery Note | Nota de entrega |
| Purchase Receipt | Recibo de compra |
| Sales Invoice / Purchase Invoice / POS Invoice | Factura de venta / Factura de compra / Factura de PDV |
| POS / Point of Sale | PDV / Punto de venta (POS Profile = Perfil de PDV) |
| Debit Note / Credit Note | Nota de débito / Nota de crédito |
| Return (noun), Is Return | Devolución, Es devolución |
| Journal Entry | Asiento contable |
| Payment Entry | Registro de pago |
| Payment Request | Solicitud de pago |
| Mode of Payment | Forma de pago |
| Cost Center | Centro de costos |
| Fiscal Year | Año fiscal |
| General Ledger / Ledger | Libro mayor |
| Party | Tercero (Party Type = Tipo de tercero) |
| Account | Cuenta |
| Amount | Monto (never "cantidad", never "importe") |
| Quantity / Qty | Cantidad / Cant. |
| Rate | depends: item price = Precio; tax rate = Tasa; exchange rate = Tipo de cambio; hourly/operating rate = Tarifa; valuation rate = Tasa de valoración |
| Valuation | Valoración |
| Reconciliation | Conciliación (Bank Reconciliation = Conciliación bancaria) |
| Grand Total | Total general |
| Write Off | Desajuste (keep upstream term) |
| Outstanding | Pendiente |
| Unpaid / Overdue | No pagado / Vencido |
| Submit / Submitted / Submittable | Validar / Validado / Validable |
| Cancel / Cancelled | Cancelar / Cancelado |
| Amend / Amended | Rectificar / Rectificado |
| Draft | Borrador |
| Report | Reporte |
| Dashboard | Tablero |
| Workspace | Área de trabajo |
| Settings | Configuración |
| Serial No | Número de serie (abbrev. "N.º de serie" only where English abbreviates) |
| Batch | Lote |
| Serial and Batch Bundle | Paquete de series y lotes |
| BOM | Lista de materiales (abbrev. LdM only when the English is a terse label like "BOM No" → "N.º de LdM") |
| UOM | UdM (Unidad de medida when spelled out) |
| Work Order | Orden de trabajo |
| Job Card | Tarjeta de trabajo |
| Workstation | Estación de trabajo |
| Material Request | Solicitud de material |
| Pick List | Lista de selección |
| Packing Slip | Lista de empaque |
| Landed Cost Voucher | Comprobante de costo de destino |
| Subcontracting | Subcontratación |
| Timesheet | Registro de horas |
| Issue (support ticket) | Incidencia ("issue" as a verb = emitir/entregar) |
| Dunning | Aviso de cobro |
| Asset / Assets | Activo / Activos (never "bienes") |
| Depreciation | Depreciación |
| Sales Person / Sales Partner | Vendedor / Socio de ventas |
| Territory | Territorio |
| Holiday List | Lista de días festivos |
| Price List / Pricing Rule | Lista de precios / Regla de precios |
| Shipping Rule | Regla de envío |
| Posting Date | Fecha de contabilización |
| Due Date | Fecha de vencimiento |
| Exchange Rate | Tipo de cambio |
| Currency | Moneda |
| Tax Id | NIT / Identificación tributaria → use "Identificación tributaria" |
