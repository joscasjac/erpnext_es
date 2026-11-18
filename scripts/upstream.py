"""Download ERPNext's and Frappe's es.po for the supported branches into scripts/.cache/."""

import os
import shutil
import subprocess
import sys
import urllib.request

BRANCHES = ("version-15", "version-16")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
URL = "https://raw.githubusercontent.com/frappe/{app}/{branch}/{app}/locale/es.po"


def path(app, branch):
	return os.path.join(CACHE, f"{app}-{branch}.po")


def download(url, dest):
	tmp = dest + ".part"
	try:
		urllib.request.urlretrieve(url, tmp)
	except OSError:
		# python.org builds on macOS often lack CA certificates; curl uses the system store.
		if not shutil.which("curl"):
			raise
		subprocess.run(["curl", "-sSfL", "-o", tmp, url], check=True)
	os.replace(tmp, dest)


def fetch(refresh=False):
	os.makedirs(CACHE, exist_ok=True)
	for app in ("erpnext", "frappe"):
		for branch in BRANCHES:
			dest = path(app, branch)
			if refresh or not os.path.exists(dest):
				print(f"downloading {app} {branch}", file=sys.stderr)
				download(URL.format(app=app, branch=branch), dest)
	return {(app, b): path(app, b) for app in ("erpnext", "frappe") for b in BRANCHES}


if __name__ == "__main__":
	fetch(refresh="--refresh" in sys.argv)
