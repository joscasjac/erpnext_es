"""Audit the Spanish ERPNext users actually see: upstream es.po with this app's es.po on top.

	python3 scripts/audit.py [--refresh]

Writes scripts/report.json and prints a summary of:
- untranslated: ERPNext strings with no Spanish (and none from Frappe either);
- problems: entries that still break a format or glossary rule;
- upstream_changed: entries this app overrides whose upstream Spanish changed since they were fixed.
Run it after an ERPNext upgrade, fix what it lists in erpnext_es/locale/es.po, and run the tests.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import po  # noqa: E402
import rules  # noqa: E402
import upstream  # noqa: E402

OURS = os.path.join(os.path.dirname(HERE), "erpnext_es", "locale", "es.po")


def upstream_note(entry):
	for c in entry["comments"]:
		if c.startswith("ERPNext: "):
			return json.loads(c[len("ERPNext: ") :])
	return None


def main():
	files = upstream.fetch(refresh="--refresh" in sys.argv)
	erp, frappe = {}, set()
	for b in upstream.BRANCHES:
		for k, e in po.read(files["erpnext", b]).items():
			if e["msgstr"] or k not in erp:
				erp[k] = e["msgstr"]
		frappe |= {k for k, e in po.read(files["frappe", b]).items() if e["msgstr"]}
	ours = po.read(OURS)
	report = collections.defaultdict(list)
	for k, up in erp.items():
		msgid, ctx = k
		mine = ours.get(k)
		es = mine["msgstr"] if mine else up
		if not es:
			if k not in frappe:
				report["untranslated"].append({"msgid": msgid, "ctx": ctx})
			continue
		why = rules.format_problems(msgid, es) + rules.style_problems(msgid, es)
		if why:
			report["problems"].append({"msgid": msgid, "ctx": ctx, "es": es, "why": why})
		if mine and upstream_note(mine) is not None and upstream_note(mine) != up:
			report["upstream_changed"].append({"msgid": msgid, "ctx": ctx, "was": upstream_note(mine), "now": up, "ours": es})
	report["not_in_erpnext"] = [{"msgid": m, "ctx": c} for (m, c) in ours if (m, c) not in erp]
	out = os.path.join(HERE, "report.json")
	json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
	print(f"ERPNext strings: {len(erp)}  overridden here: {len(ours)}")
	for k in ("untranslated", "problems", "upstream_changed", "not_in_erpnext"):
		print(f"  {k}: {len(report[k])}")
	c = collections.Counter(w for p in report["problems"] for w in p["why"])
	for w, n in c.most_common():
		print(f"    {n:5}  {w}")
	print(f"details: {out}")


if __name__ == "__main__":
	main()
