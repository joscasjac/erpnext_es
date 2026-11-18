"""Checks shared by audit.py and the tests. Each check gets the English msgid and the Spanish msgstr."""

import re

PLACEHOLDER = re.compile(r"\{\{.*?\}\}|\{%.*?%\}|\{[^{}\s]*\}|%\([a-z_]+\)s|%[sd]")
TAG = re.compile(r"<[^>]+>")
_ATTR = re.compile(r"\s+(title|alt|placeholder|aria-label)=\"[^\"]*\"")

# (pattern in the English, pattern that must not appear in the Spanish, glossary rule)
_I, _C = re.I, 0
GLOSSARY = [
	(r"\bitems?\b", _I, r"\belementos?\b|\bítems?\b|\bitems?\b", _I, "Item = artículo"),
	(r"\bitems?\b(?! bundle)", _I, r"\bproductos?\b", _I, "Item = artículo"),
	(r"\bstock\b", _I, r"\bstock\b", _I, "Stock = inventario / existencias"),
	(r"^stock$|\bstock (entry|ledger|settings|reconciliation)", _I, r"almac[eé]n", _I, "Stock is not almacén"),
	(r"\bquotations?\b", _I, r"presupuesto", _I, "Quotation = cotización"),
	(r"\bleads?\b", _I, r"conductor|iniciativa|\blead", _I, "Lead = cliente potencial"),
	(r".", _I, r"compañ[ií]a", _I, "Company = empresa"),
	(r"\bsubmit", _I, r"\benvi[aá]|present[aá]", _I, "Submit = validar"),
	(r"\bamend", _I, r"modific|corregi|enmend", _I, "Amend = rectificar"),
	(r".", _I, r"albar[aá]n|pedidos? de (venta|compra)", _I, "Spain-only term"),
	(r".", _I, r"\(OV\)|\(OC\)", _C, "no (OV)/(OC) suffix"),
	(r".", _I, r"\bcostes?\b", _I, "coste = costo"),
	(r"journal entr", _I, r"entradas? de diario|asientos? de diario", _I, "Journal Entry = asiento contable"),
	(r"payment entr", _I, r"entradas? de pago", _I, "Payment Entry = registro de pago"),
	(r"serial no", _I, r"\bno\.? de serie|nº serie", _I, "Serial No = número de serie"),
	(r"\bBOMs?\b", _C, r"\bBOMs?\b", _C, "BOM = lista de materiales / LdM"),
	(r"material request", _I, r"requisici", _I, "Material Request = solicitud de material"),
	(r".", _I, r"\bTPV\b", _C, "POS = PDV"),
	(r"\bPOS\b", _C, r"\bPOS\b|\bPdV\b", _C, "POS = PDV"),
	(r"general ledger", _I, r"balance general", _I, "General Ledger = libro mayor"),
	(r"\bworkstations?\b", _I, r"puestos? de trabajo", _I, "Workstation = estación de trabajo"),
	(r"\bUOMs?\b", _C, r"\bUOMs?\b", _C, "UOM = UdM"),
	(r"\bpart(y|ies)\b", _I, r"\bpartes?\b", _I, "Party = tercero"),
	(r"timesheet", _I, r"parte de horas|hoja de tiempo", _I, "Timesheet = registro de horas"),
	(r"packing slip", _I, r"embalaje", _I, "Packing Slip = lista de empaque"),
	(r"\bdunning", _I, r"reclamaci", _I, "Dunning = aviso de cobro"),
	(r"\bassets?\b", _I, r"\bbienes\b", _I, "Asset = activo"),
	(r"^bin$", _I, r"papelera", _I, "Bin is a stock record, not a trash can"),
	(r"reconcil", _I, r"reconcilia", _I, "Reconciliation = conciliación"),
	(r"\bamounts?\b", _I, r"\bimportes?\b|\bcantidad", _I, "Amount = monto"),
	(r"\breports?\b", _I, r"\binformes?\b", _I, "Report = reporte"),
	(r"\bdashboards?\b", _I, r"\bpanel", _I, "Dashboard = tablero"),
	(r"mode of payment", _I, r"modos? de pago", _I, "Mode of Payment = forma de pago"),
	(r"customer group|supplier group", _I, r"categor[ií]a", _I, "Group = grupo"),
	(r"\bfiscal year", _I, r"\bejercicio", _I, "Fiscal Year = año fiscal"),
	(r"\breturns?\b", _I, r"\bretorn", _I, "Return = devolución"),
	(r"\bunpaid\b", _I, r"impagad", _I, "Unpaid = no pagado"),
	(r"grand total", _I, r"^total$", _I, "Grand Total = total general"),
	(r"sales person", _I, r"persona de ventas", _I, "Sales Person = vendedor"),
	(r".", _I, r"ordenador|fichero|\bpulse\b|\bpulsa\b", _I, "Spain-only term"),
	(r".", _I, r"\b(de|la|el|los|las|en|que|del|y)\s+\1\b", _I, "repeated word"),
	(
		r".",
		_I,
		r"\b(debito|credito|inspeccion|configuracion|informacion|transaccion|numero|codigo|articulos?|almacen|categoria|direccion|valido|electronico|automatico|razon|operacion|depreciacion|cancelacion|validacion|creacion|aplicacion|condicion|ubicacion|descripcion|seleccion|devolucion|cotizacion|conciliacion)\b",
		_I,
		"missing accent",
	),
	(
		r".",
		_I,
		r"(?<!se )\b(seleccione|introduzca|ingrese|agregue|añada|establezca|verifique|revise|intente|elija|asegúrese|haga clic|póngase|comuníquese|usted|ustedes)\b",
		_I,
		"usted register (use tú)",
	),
]
GLOSSARY = [(re.compile(a, af), re.compile(b, bf), why) for a, af, b, bf, why in GLOSSARY]

_SMALL = {"de", "del", "la", "las", "el", "los", "y", "o", "en", "por", "para", "a", "al", "con", "sin", "un", "una"}


def _tags(s):
	return sorted(_ATTR.sub("", t) for t in TAG.findall(s))


def format_problems(msgid, msgstr):
	"""Problems that break rendering: placeholders, markup, newlines, edge whitespace."""
	out = []
	if sorted(PLACEHOLDER.findall(msgid)) != sorted(PLACEHOLDER.findall(msgstr)):
		out.append("placeholder mismatch")
	if _tags(msgid) != _tags(msgstr):
		out.append("markup mismatch")
	if msgid.count("\n") != msgstr.count("\n"):
		out.append("newline count")
	if msgid[:1].isspace() != msgstr[:1].isspace() or msgid[-1:].isspace() != msgstr[-1:].isspace():
		out.append("edge whitespace")
	return out


def title_case(msgstr):
	words = re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñü]+", msgstr)
	if len(words) < 3 or len(msgstr) > 60:
		return False
	rest = [w for w in words[1:] if w.lower() not in _SMALL]
	caps = [w for w in rest if w[0].isupper() and not w.isupper()]
	return bool(caps) and len(caps) == len(rest)


def style_problems(msgid, msgstr):
	out = [why for en, es, why in GLOSSARY if en.search(msgid) and es.search(msgstr)]
	if title_case(msgstr):
		out.append("title case")
	return list(dict.fromkeys(out))
