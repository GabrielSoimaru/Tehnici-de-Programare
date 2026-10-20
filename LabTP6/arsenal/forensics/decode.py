#A1 - A7
import re
import base64
from urllib.parse import unquote
import hashlib
import argparse
import json

s = "Salut"
b = s.encode() # bytes
print(b, b[0]) # b"Salut" 83
# TODO: tipareste b.hex() si refa bytes din hex cu bytes.fromhex(...)
h = b.hex()
print(h)
print(bytes.fromhex(h))

def ghici_strat(s):
    # TODO: daca are %xx -> "url"
    if re.search(r'%[0-9a-fA-F]{2}', s):
        return "url"
    # TODO: daca doar 0-9 a-f si lungime para -> "hex"
    if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
        return "hex"
    # TODO: daca doar A-Za-z0-9+/= -> "base64"
    if re.fullmatch(r'[A-Za-z0-9+/=]+', s):
        return "base64"
    return "necunoscut"
print(ghici_strat("%2Fetc")) # url
print(ghici_strat("48656c6c6f")) # hex
print(ghici_strat("U2FsdXQ=")) # base64

def desfa(s):
    strat = ghici_strat(s)
    # TODO: pentru fiecare strat, decodeaza
    # base64 -> base64.b64decode(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    # hex -> bytes.fromhex(s)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    # url -> unquote(s).encode()
    if strat == "url":
        return strat, unquote(s).encode()
    # intoarce (strat, rezultat_bytes)
    return strat, s.encode()
print(desfa("%2Fetc")) # url
print(desfa("48656c6c6f")) # hex
print(desfa("U2FsdXQ=")) # base64

def citibil(b):
    # TODO: True daca toti octetii sunt 32..126
    return all(32 <= c < 127 for c in b)

if __name__ == "__main__":
    val = open("probe/mesaj.txt").read().strip()
    for _ in range(8):
        strat, b = desfa(val)
        # TODO: daca citibil(b): opreste si tipareste
        # altfel val = b.decode(); continua
        if citibil(b) and ghici_strat(b.decode()) == "necunoscut":
            print(b)
            break
        else:
            val = b.decode()

    date = open("probe/xor.bin", "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        # TODO: daca citibil(clar):
        # print("cheie:", k, clar.decode())
        if citibil(clar):
            print("cheie:", k, clar.decode())
            break

    tinta = open("probe/hashuri.txt").readline().strip()
    print(len(tinta)) # 32 md5 / 40 sha1 / 64 sha256
    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()
    # TODO: daca hashlib.md5(cuv.encode()).hexdigest()
    # == tinta: print("gasit:", cuv); break 
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("gasit:", cuv)
            break

    p = argparse.ArgumentParser()
    p.add_argument("intrare") # sir sau cale
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()
    # TODO: daca a.fisier, citeste octetii din cale;
    # altfel trateaza intrarea ca sir
    if a.fisier:
        val = open(a.intrare, "rb").read().decode().strip()
    else:
        val = a.intrare
    # TODO: salveaza {strat, rezultat} in
    # arsenal/forensics/fisa.json
    for _ in range(8):
        strat, b = desfa(val)
        if citibil(b) and ghici_strat(b.decode()) == "necunoscut":
            break
        else:
            val = b.decode()
    rezultat = b.decode()
    date = {
        "strat": strat,
        "rezultat": rezultat
    }
    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump(date, f)