#Lucrarea A
#A1
from dataclasses import dataclass, asdict
import json
# @dataclass
# class Proces:
#     pid: int
#     nume: str
#     user: str
#     cale: str

# p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
# print(p.pid, p.nume)
# print(p)

#A2
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

@dataclass
class Proces:
    pid: int; nume: str; user: str; cale: str
    def e_suspect(self):
        # TODO: True daca una din CAI_SUSPECTE e in self.cale
        for x in CAI_SUSPECTE:
            if x in self.cale:
                return True
        return False


# p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
# print(p.e_suspect()) # True (update.exe din Temp)

#A3
SUSPECTE_ID = {4625, 1102, 7045}

@dataclass
class Eveniment:
    id: int; nivel: str; sursa: str; cont: str; mesaj: str
    def e_suspect(self):
        # TODO: True daca self.id in SUSPECTE_ID SAU self.nivel == "critical"
        if self.id in SUSPECTE_ID or self.nivel == "critical":
            return True
        else:
            return False

# e1 = Eveniment(4625, "warning", "Security", "administrator", "Logon esuat")
# print(f"Test 1 (ID 4625): {e1.e_suspect()}")

# e2 = Eveniment(9999, "critical", "System", "SYSTEM", "Eroare severa")
# print(f"Test 2 (Nivel critical): {e2.e_suspect()}")

# e3 = Eveniment(1000, "info", "System", "user1", "Totul ok")
# print(f"Test 3 (Inofensiv): {e3.e_suspect()}")

#A4
# def procese_din_json(cale):
#     with open(cale, encoding="utf-8") as f:
#         # TODO: intoarce [Proces(**d) for d in json.load(f)]
#         return [Proces(**d) for d in json.load(f)]

# procese = procese_din_json("arsenal/windows/start/procese.json")
# print("procese:", len(procese))
# print("suspecte:", sum(1 for p in procese if p.e_suspect()))

#Lucrarea B
#B1
@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            # TODO: return cls([Proces(**d) for d in json.load(f)])
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)
    
    #B2
    def suspecte(self):
        # TODO: lista proceselor cu p.e_suspect()
        ls = []
        for p in self.procese:
            if p.e_suspect():
                ls.append(p)
        return ls
    def pe_user(self):
        # TODO: dict user -> lista de nume (foloseste setdefault)
        users = {}
        for p in self.procese:
            users.setdefault(p.user, [])
            users[p.user].append(p.nume)
        return users

inv = Inventar.din_json("arsenal/windows/start/procese.json")
# print("procese:", len(inv))

# B2
# for p in inv.suspecte():
#     print(f" [{p.pid}] {p.nume} {p.cale}")
# print(inv.pe_user())

#B3
from dataclasses import asdict

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce [Proces(**d) for d in json.load(f)]
        return [Eveniment(**d) for d in json.load(f)]

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    alarma = [e for e in ev if e.e_suspect()]
    # TODO: cu --json, json.dumps cu asdict pe suspecte si alarma;
    # fara, un rezumat citibil
    if a.json:
        raport = {
           "suspecte": [asdict(x) for x in inv.suspecte()],
           "alarma": [asdict(e) for e in alarma]
        }
        print(json.dumps(raport, indent=2))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}")
        for p in inv.suspecte():
            print(f" [{p.pid}] {p.nume} {p.user} {p.cale}")
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f" {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()