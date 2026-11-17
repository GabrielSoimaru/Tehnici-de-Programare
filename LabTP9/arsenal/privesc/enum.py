#A1
import argparse, json, os
def citeste_linii(cale):
    linii = []
    with open(cale, encoding="utf-8") as f:
        for x in f:
            x = x.strip()
            if x and not x.startswith("#"):
                linii.append(x)
    return linii

# cai = citeste_linii("arsenal/privesc/start/suid.txt")
# print("linii SUID:", len(cai))

#A2
def nume(cale):
    bucati = cale.rsplit("/", 1)
    rez = bucati[-1]
    return rez

# nume_unice = {nume(c) for c in cai} # set comprehension
# print("SUID distincte:", len(nume_unice))

#A3
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
"less", "awk", "python3", "perl"}

def suid_constatari(cale):
    cai = citeste_linii(cale)
    lista = set(cai)
    rez = []
    for c in sorted(lista):
        x = {"cale": c, "nume": nume(c), "risc": "mare" if nume(c) in GTFO else "normal"}
        rez.append(x)
    return rez

# suid = suid_constatari("arsenal/privesc/start/suid.txt")
# mari = [c for c in suid if c["risc"] == "mare"] 
# print(len(suid), "SUID,", len(mari), "cu risc mare")
# print(sorted(c["nume"] for c in mari))

#A4
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1) # despachetare in tuplu
        out.append({"user": user.strip(), "drept": drept.strip(), "risc": "mare" if "NOPASSWD" in drept else "normal"})
    return out

def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        rez = {"user": user, "comanda": comanda}
        out.append(rez)
    return out

def enumereaza(d):
    return {
    "suid": suid_constatari(os.path.join(d, "suid.txt")),
    "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
    "cron": cron_constatari(os.path.join(d, "crontab.txt")),
}

# print(enumereaza("arsenal/privesc/start"))

#A5
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    users_sudo = {u["user"] for u in raport["sudo"]}
    users_cron = {u["user"] for u in raport["cron"]}
    users = users_sudo | users_cron
    print(f"utilizatorii implicati: {", ".join(sorted(users))}")
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")

if __name__ == "__main__":
    main()