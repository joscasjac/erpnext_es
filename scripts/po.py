"""Small .po reader/writer (msgctxt, msgid, msgstr, extracted comments; no plurals). Stdlib only."""

import ast


def read(path):
	"""Return {(msgid, msgctxt): {"msgstr": str, "comments": [str], "refs": [str], "fuzzy": bool}}."""
	entries = {}
	cur, key = {}, None

	def flush():
		if cur.get("msgid"):
			entries[(cur["msgid"], cur.get("msgctxt"))] = {
				"msgstr": cur.get("msgstr", ""),
				"comments": cur.get("comments", []),
				"refs": cur.get("refs", []),
				"fuzzy": cur.get("fuzzy", False),
			}

	for raw in open(path, encoding="utf-8"):
		line = raw.rstrip("\n")
		if not line.strip():
			flush()
			cur, key = {}, None
			continue
		if line.startswith("#~"):
			continue
		if line.startswith("#"):
			if "msgid" in cur and key != "msgctxt":
				flush()
				cur, key = {}, None
			if line.startswith("#. "):
				cur.setdefault("comments", []).append(line[3:])
			elif line.startswith("#: "):
				cur.setdefault("refs", []).extend(line[3:].split())
			elif line.startswith("#,") and "fuzzy" in line:
				cur["fuzzy"] = True
			continue
		for k in ("msgctxt", "msgid_plural", "msgid", "msgstr[0]", "msgstr"):
			if line.startswith(k + " "):
				if k in ("msgid", "msgctxt") and "msgstr" in cur:
					flush()
					cur = {}
				key = {"msgstr[0]": "msgstr"}.get(k, k)
				cur[key] = ast.literal_eval(line[len(k) + 1 :])
				break
		else:
			if line.startswith('"') and key:
				cur[key] += ast.literal_eval(line)
	flush()
	return entries


def esc(s):
	return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r") + '"'


def field(name, s):
	if "\n" not in s.rstrip("\n"):
		return f"{name} {esc(s)}\n"
	parts = s.split("\n")
	lines = [p + "\n" for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])
	return f'{name} ""\n' + "".join(esc(x) + "\n" for x in lines)


HEADER = """# Corrected Spanish (Latin America) translation of ERPNext.
# Overrides ERPNext's own es.po; see README.md.
# This file is distributed under the same license as ERPNext (GPL-3.0).
#
msgid ""
msgstr ""
"Project-Id-Version: erpnext_es\\n"
"PO-Revision-Date: 2026-11-17 00:00+0000\\n"
"Last-Translator: Quest Media Hub\\n"
"Language: es\\n"
"Language-Team: Spanish (Latin America)\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

"""


def write(path, entries):
	"""entries: iterable of dicts with msgid, msgctxt, msgstr, comments, refs."""
	with open(path, "w", encoding="utf-8") as f:
		f.write(HEADER)
		for e in entries:
			for c in e.get("comments", []):
				f.write(f"#. {c}\n")
			if e.get("refs"):
				f.write("#: " + " ".join(e["refs"]) + "\n")
			if e.get("msgctxt"):
				f.write(field("msgctxt", e["msgctxt"]))
			f.write(field("msgid", e["msgid"]))
			f.write(field("msgstr", e["msgstr"]))
			f.write("\n")
