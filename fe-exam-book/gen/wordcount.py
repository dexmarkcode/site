import re, glob, os
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "src", "*.md"))):
    t = open(f).read()
    t = t.replace("\\$", "USD")
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " x ", t)
    t = re.sub(r"\{\{.*?\}\}", " ", t)
    print(os.path.basename(f), len(re.findall(r"[A-Za-z’'-]+", t)))
