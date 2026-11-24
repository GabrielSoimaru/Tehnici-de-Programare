#A1
MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}
def tip(head): 
    for id, name in MAGIC.items():
        if head.startswith(id):
            return name
    return "necunoscut"

# print(tip(b"\x89PNG\r\n"), tip(b"%PDF-1.4"), tip(b"text"))

#A2
import os, hashlib
def amprenta_fisier(cale):
    with open(cale, "rb") as f:
        date = f.read()
    return {"nume": os.path.basename(cale), "tip": tip(date[:8]), "sha256": hashlib.sha256(date).hexdigest()[:16]}

# print(amprenta_fisier("arsenal/forensics/probe/imagine.png"))

#A3
def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("folder")
    a = p.parse_args()
    for x in scaneaza(a.folder):
        print(f"{x['nume']:14} {x['tip']:11} {x['sha256']}")

if __name__ == "__main__":
    main()