"""Builds the offline 'app' copy of the guide from index.html.
Run from the project folder:  python3 tools/build_app.py

The downloaded copy is a single file, so it drops the links to the
manifest and icon files (which only exist on the website)."""
import re
from pathlib import Path
root = Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text(encoding="utf-8")
marker = 'window.GUIDE_MODE = "web";'
assert marker in src, "mode marker missing from index.html"
out = src.replace(marker, 'window.GUIDE_MODE = "app";')
out, n = re.subn(r"<!--pwa-->.*?<!--/pwa-->\n?", "", out, flags=re.S)
assert n == 1, "pwa block markers missing from index.html"
(root / "Aldersgate-AI-Guide-App.html").write_text(out, encoding="utf-8")
print("Wrote Aldersgate-AI-Guide-App.html", len(out.encode()) // 1024, "KB")
print("Reminder: if you changed index.html, bump VERSION in sw.js so phones get the update.")
