# ERPNext Español

Corrected Latin American Spanish for [ERPNext](https://github.com/frappe/erpnext), shipped as its own Frappe app. ERPNext's code and its own `es.po` are not changed.

- **Built from ERPNext v15 and v16** (`version-15` and `version-16` branches, 13,015 strings between them).
- **`erpnext_es/locale/es.po` holds 7,628 entries:** 5,808 corrections to ERPNext's Spanish and 1,820 strings ERPNext had left in English. Strings ERPNext already translates well are left to it.
- **Every entry records what ERPNext had** (`#. ERPNext: "..."`), so a reviewer can compare and `scripts/audit.py` can tell when upstream changes.
- **Works for `es` and every `es-*` dialect** (es-GT, es-MX…). Frappe loads the base language first and puts the dialect on top.

## What it fixes

Problems found in ERPNext's upstream `es.po`:

| Problem | Examples (English → ERPNext's Spanish) |
|---|---|
| Wrong DocType names, shown all over the UI | Item → *Elemento*; Stock → *Almacén* (the same word as Warehouse); General Ledger → *Balance general* (that is the Balance Sheet); Bin → *Papelera* (trash can); Assets → *Bienes* |
| Wrong meanings | Outstanding → *Excepcional*; Total Liability → *Responsabilidad total*; Writeoff → *Pedir por escrito*; Leads → *conductores*; Quotations → *Citas*; Revenue → *Ganancia*; Blanket Order → *Orden de la Manta*; Plaid → *a cuadros*; Consumed Quantity → *Calidad consumida* |
| One concept, many words | Item as *producto*, *elemento* or *artículo*; Quotation as *cotización* or *presupuesto* (which is Budget); Amount as *importe*, *monto* or *cantidad* (which is Quantity); POS as *TPV*, *PdV* or *POS* |
| Spain-only wording | *compañía*, *coste*, *albarán*, *pedido de venta*, *pulse*, *ordenador*, *NIF/CIF* |
| Mixed register | *tú* and *usted* in the same screens; everything now uses *tú* ("Selecciona", "tu empresa", "para ti") |
| English Title Case | *Saldo en Moneda de la Cuenta* |
| Broken strings | placeholders out of order or lost (`{0}` twice instead of `{0} {1}`), newlines replaced by ` \| `, trailing spaces dropped, typos (*Procentaje*, *Fuente de de*), text left in English |
| Untranslated | 1,820 strings, mostly new in v16 (onboarding, help texts, messages) |

The rules the fixes follow are in [GLOSSARY.md](GLOSSARY.md): neutral Latin American Spanish, informal *tú* (like the FAC app), sentence case, and one Spanish term per ERPNext concept. Where Frappe already settles a term, this app uses Frappe's word (Submit = *Validar*, Amend = *Rectificar*, Report = *Reporte*, Dashboard = *Tablero*).

Main renamed DocTypes:

| English | ERPNext had | Now |
|---|---|---|
| Item | Elemento / Producto | Artículo |
| Stock Entry | Entradas de inventario | Movimiento de inventario |
| General Ledger | Balance general | Libro mayor |
| Sales Order / Purchase Order | Orden de venta (OV) / Orden de compra (OC) | Orden de venta / Orden de compra |
| Supplier Quotation | Presupuesto de Proveedor | Cotización de proveedor |
| Lead | Iniciativa | Cliente potencial |
| Payment Entry | Entrada de pago | Registro de pago |
| POS Invoice | Factura PdV | Factura de PDV |
| Dunning | Reclamación | Aviso de cobro |
| Bin | Papelera | Existencias por almacén |

## How it works

Frappe builds each language's dictionary by merging the catalogs of the installed apps in install order, so a later app's entry wins. `erpnext` is in this app's `required_apps`, so this app is always installed after ERPNext and its `es.po` overrides ERPNext's for the strings it lists. Translations a user adds in the **Translation** DocType still win over both.

Because the merge is by source string, an entry also applies to any other app that uses the same English (for example "Items" in Frappe itself). That is intended: the same word reads the same everywhere.

## Install

```bash
bench get-app <this repo>
```

```bash
bench --site <site> install-app erpnext_es
```

```bash
bench build --app erpnext_es
```

`bench build` compiles `es.po` to `.mo`; `bench compile-po-to-mo --app erpnext_es` does the same. Users see the corrected Spanish once their **Language** (or the site's) is `es` or an `es-*` dialect. If old text is still cached, run `bench --site <site> clear-cache`.

To go back to ERPNext's own Spanish, uninstall the app (`bench --site <site> uninstall-app erpnext_es`) and clear the cache.

## After an ERPNext upgrade

```bash
python3 scripts/audit.py --refresh
```

It downloads ERPNext's and Frappe's current `es.po` for v15 and v16, applies this app's catalog on top, and writes `scripts/report.json` with:

- `untranslated`: ERPNext strings nobody translates;
- `problems`: strings that still break a placeholder, markup or glossary rule (the glossary checks are heuristics, so read each one; many are fine, e.g. *producto terminado* for Finished Good);
- `upstream_changed`: strings this app overrides whose ERPNext Spanish changed since they were fixed, so you can check whether upstream caught up;
- `not_in_erpnext`: entries here whose English no longer exists in ERPNext.

Fix what it lists in `erpnext_es/locale/es.po`, keeping the `#. ERPNext:` line, then run the tests.

## Tests

```bash
python3 -m unittest discover -s tests
```

No bench needed. They check that every entry is translated, keeps its placeholders, markup, newlines and edge spaces, records what ERPNext had, uses no Spain-only words, and that the main DocType names are right. With Babel installed (any bench has it) they also compile the catalog.

## Known limits

- Some ERPNext messages are built from pieces in code ("{0} {1} created"), so word order and gender can still read awkwardly in a few places.
- Strings that ERPNext does not mark for translation stay in English. That has to be fixed in ERPNext itself.
- HRMS, Frappe CRM, Helpdesk and other apps are not covered, except where they share an English string with ERPNext.

## Contributing

Corrections are welcome. Edit `erpnext_es/locale/es.po` following [GLOSSARY.md](GLOSSARY.md), keep the `#. ERPNext:` line, run the tests and open a pull request.

## License

[GPL-3.0](license.txt), the same license as ERPNext, whose Spanish catalog this work builds on. Anyone may use, copy, change and redistribute it for free, including in commercial deployments; redistributed changes must stay under GPL-3.0.
