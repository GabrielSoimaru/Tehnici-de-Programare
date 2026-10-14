# Laborator: funcții, metode și importuri pe web
# Student: Șoimaru Gabriel
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 3  # secunde

import requests
import time

# Exercițiul 9
print("Exercițiul 9")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print(response.status_code) # atribut
print(response.ok) # atribut
print(response.url) # atribut
print(response.encoding) # atribut

time.sleep(1)

# Exercițiul 10
print("Exercițiul 10")
response.raise_for_status()
try:
    requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
except requests.HTTPError:
    print("A avut loc o eroare. Mai incearcă odată.")

# Exercițiul 11
print("Exercițiul 11")
for x, y in response.headers.items():
    print(f"{x}: {y}")

# Exercițiul 12
print("Exercițiul 12")
print(response.headers.get("Server", "lipsește"))
print(response.headers.get("Content-Type", "lipsește"))
print(response.headers.get("content-type"))
# Obervație: Nu conteză dacă e majusculă sau nu, get() va da același raspuns

# Exercițiul 13
print("Exercițiul 13")
print(response.text.lower().count("cyber"))
# .lower() și .count() pot fi înlănțuite deoarece .lower() returnează același obiect modificat care poate fi folosit de .count()

# Exercițiul 14
print("Exercițiul 14")
start = response.text.find("<title>") + len("<title>")
end = response.text.find("</title>")
print(response.text[start:end].strip())

# Exercițiul 15
print("Exercițiul 15")
lines = response.text.splitlines()
print(len(lines))
print(len(max(lines, key=len)))

# Exercițiul 16
print("Exercițiul 16")
if response.url.startswith("https://"):
    print("Conexiunue securizată")
else:
    print("Conexiune nesecurizată")

# Exercițiul 17
print("Exercițiul 17")
response = requests.get("http://cybercor.org", timeout=TIMEOUT)
for x in response.history:
    print(x.url)
    print(x.status_code)
print(response.url)

time.sleep(1)

# Exercițiul 18
print("Exercițiul 18")
response = requests.head(BASE_URL)
print(len(response.content))
time.sleep(1)
response = requests.get(BASE_URL)
print(len(response.content))
# .get primește tot conținutul fișierului html, în timp ce .head primește doar headers și status code deci nu are conținut

time.sleep(1)

# Exercițiul 19
print("Exercițiul 19")
response = requests.get(BASE_URL, timeout=TIMEOUT)
if len(response.cookies) > 0:
    for x in response.cookies:
        print(x.name)
        print(x.secure)
else:
    print("Niciun cookie setat")

time.sleep(1)

# Exercițiul 20
print("Exercițiul 20")
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Soimaru Gabriel"})
response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print(response.text)
# .json() are paranteze deoarece este o metoda in timp ce .text este un atribut si nu are nevoie de paranteze