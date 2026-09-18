import sys, xml.etree.ElementTree as ET
ns={"a":"http://www.w3.org/2005/Atom"}
data=sys.stdin.read()
try: root=ET.fromstring(data)
except Exception as e:
    print("  parse err",e); sys.exit()
entries=root.findall("a:entry",ns)
if not entries: print("  (no results)")
for e in entries:
    t=" ".join(e.find("a:title",ns).text.split())
    idu=e.find("a:id",ns).text
    pub=e.find("a:published",ns).text[:10]
    au=[a.find("a:name",ns).text for a in e.findall("a:author",ns)]
    summ=" ".join((e.find("a:summary",ns).text or "").split())
    print("  " + pub + " | " + t)
    print("     " + idu + " | " + ", ".join(au[:5]))
    print("     ABS: " + summ[:400])
    print()
