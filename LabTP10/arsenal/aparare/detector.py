#B1
def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    out = []
    for ip, n in counts.items():
        if n >= prag:
            out.append((ip, n))
    return sorted(out, key = lambda x: x[1], reverse=True)

# from collections import Counter
# c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
# print(suspecti(c))
# print(suspecti(c, prag=2))

#B3
import argparse, json
from collections import Counter
from arsenal.aparare.parse_auth import citeste_esecuri
def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)
    out = {
        "esecuri": esecuri, 
        "pe_ip": counts,
        "suspecti": sus
        }
    if a.json:
        print(json.dumps(out, indent=2)); return
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f"  {ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"  {ip} ({n} incercari) BRUTE FORCE")

if __name__ == "__main__":
    main()