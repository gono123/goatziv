"""python3 fixd.py <file> name=d ... : set the push() distance inside the named shot functions."""
import re, sys
f = sys.argv[1]; src = open(f).read()
for kv in sys.argv[2:]:
    name, d = kv.split("=")
    m = re.search(rf"\ndef {name}\(S\):\n(.*?)(?=\ndef |\nALIASES)", src, re.S)
    body = m.group(1)
    nb = re.sub(r"push\(S, (\([^)]*\)), [\d.]+", rf"push(S, \1, {d}", body, count=1)
    assert nb != body, name
    src = src.replace(body, nb)
open(f, "w").write(src)
