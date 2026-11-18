"""Offline checks of erpnext_es/locale/es.po. No bench needed:

	python3 -m unittest discover -s tests
"""

import io
import json
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import po  # noqa: E402
import rules  # noqa: E402

PO = os.path.join(ROOT, "erpnext_es", "locale", "es.po")
ENTRIES = po.read(PO)
# Words that are never right in this catalog, whatever the English says.
NEVER = re.compile(r"compañ[ií]a|\bTPV\b|\bcostes?\b|\(OV\)|\(OC\)|albar[aá]n|ordenador|fichero", re.I)
USTED = re.compile(r"(?<!se )\b(usted|ustedes|seleccione|ingrese|introduzca|agregue|asegúrese|haga clic|póngase|comuníquese)\b", re.I)


class Catalog(unittest.TestCase):
	def test_has_entries(self):
		self.assertGreater(len(ENTRIES), 3000)

	def test_no_duplicates(self):
		with open(PO, encoding="utf-8") as f:
			text = f.read()
		blocks = [b for b in text.split("\n\n") if "\nmsgid " in "\n" + b and 'msgid ""\nmsgstr ""\n"Project' not in b]
		self.assertEqual(len(blocks), len(ENTRIES))

	def test_every_entry_is_translated(self):
		for (msgid, ctx), e in ENTRIES.items():
			with self.subTest(msgid=msgid, ctx=ctx):
				self.assertTrue(e["msgstr"].strip())
				self.assertFalse(e["fuzzy"])

	def test_placeholders_markup_and_spacing_survive(self):
		for (msgid, ctx), e in ENTRIES.items():
			with self.subTest(msgid=msgid, ctx=ctx):
				self.assertEqual(rules.format_problems(msgid, e["msgstr"]), [])

	def test_no_spain_only_or_banned_words(self):
		for (msgid, ctx), e in ENTRIES.items():
			with self.subTest(msgid=msgid, ctx=ctx):
				self.assertIsNone(NEVER.search(e["msgstr"]))

	def test_tu_register(self):
		for (msgid, ctx), e in ENTRIES.items():
			with self.subTest(msgid=msgid, ctx=ctx):
				self.assertIsNone(USTED.search(e["msgstr"]))

	def test_every_entry_records_what_erpnext_had(self):
		for (msgid, ctx), e in ENTRIES.items():
			with self.subTest(msgid=msgid, ctx=ctx):
				notes = [c for c in e["comments"] if c.startswith("ERPNext: ")]
				self.assertEqual(len(notes), 1)
				self.assertIsInstance(json.loads(notes[0][len("ERPNext: ") :]), str)

	def test_core_doctype_names(self):
		expected = {
			"Item": "Artículo",
			"Stock Entry": "Movimiento de inventario",
			"General Ledger": "Libro mayor",
			"Bin": "Existencias por almacén",
			"Sales Order": "Orden de venta",
			"Purchase Order": "Orden de compra",
			"Supplier Quotation": "Cotización de proveedor",
			"Lead": "Cliente potencial",
			"Payment Entry": "Registro de pago",
			"Assets": "Activos",
		}
		for msgid, es in expected.items():
			with self.subTest(msgid=msgid):
				self.assertEqual(ENTRIES[msgid, None]["msgstr"], es)

	def test_compiles_with_babel(self):
		try:
			from babel.messages.mofile import write_mo
			from babel.messages.pofile import read_po
		except ImportError:
			self.skipTest("babel not installed (bench has it)")
		with open(PO, "rb") as f:
			catalog = read_po(f)
		buf = io.BytesIO()
		write_mo(buf, catalog)
		self.assertGreater(len(buf.getvalue()), 1000)


if __name__ == "__main__":
	unittest.main()
