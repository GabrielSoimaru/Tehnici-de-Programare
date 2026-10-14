# Laborator: funcții, metode și importuri pe web
# Student: Șoimaru Gabriel
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 3  # secunde

import requests
import time


# Exercițiul 21
print("Exercițiul 21")
def fetch(url):
    """ Returneaza obiectul raspuns dupa .get
    Primeste adresa in forma de string """
    response = requests.get(url, timeout=TIMEOUT)
    return response

print(fetch(BASE_URL).status_code)

# Exercițiul 22
print("Exercițiul 22")
def get_status(url): 
   """ Returneaza codul de stare a obiectului raspuns dupa .get
   Primeste adresa in forma de string """
   response = requests.get(url, timeout=TIMEOUT)
   return response.status_code
    
print(get_status(BASE_URL + "/"))
time.sleep(1)
print(get_status(BASE_URL + "/robots.txt"))
time.sleep(1)
print(get_status(BASE_URL + "/sitemap.xml"))

# Exercițiul 23
print("Exercițiul 23")
def fetch(url, timeout = 10):
    """ Returneaza obiectul raspuns dupa .get
    Primeste adresa in forma de string """
    response = requests.get(url, timeout=timeout)
    return response

fetch(BASE_URL, timeout = 10)
time.sleep(1)
fetch(BASE_URL, timeout = 3)

# Exercițiul 24
print("Exercițiul 24")
def get_title(html):
    """ Returneaza titlul fisierului html introdus
    Primeste fisierul html (textul din raspunsul de dupa .get) """
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

response = fetch(BASE_URL, timeout=TIMEOUT)
print(get_title(response.text))

# Exercițiul 25
print("Exercițiul 25")
help(get_title)

# Exercițiul 26
print("Exercițiul 26")
def get_status(url: str) -> int:
    """ Returneaza codul de stare a obiectului raspuns dupa .get
    Primeste adresa in forma de string """
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

# get_status(123)
# Observație: Nu, adnotările de tip nu opresc execuția, ci doar dau o sugestie, un hint despre tipul necesar is cel la final, deci preogramul va rula și va da eroare

# Exercițiul 27
print("Exercițiul 27")
def page_exists(url):
    """ Verifica daca există pagina și returneaza True sau False 
    Primeste adresa in forma de string """
    try:
        requests.get(url, timeout=TIMEOUT)
        return True
    except requests.RequestException:
        return False

print(page_exists(BASE_URL))
time.sleep(1)
print(page_exists("https://this-domain-does-not-exist.invalid"))

# Exercițiul 28
print("Exercițiul 28")
def check_paths(base, paths):
    """ Returneaza nu dictionar format din linkul de baza si stringurile din lista primita
    Primeste adresa in forma string si o lista cu stringuri """
    rez = {}
    for x in paths:
        y = get_status(base + x)
        time.sleep(1)
        rez[base + x] = y
    return rez

print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"])) 

# Exercițiul 29
print("Exercițiul 29")
def get_header(url, name, default="lipsește"):
    """ Returneaza valoarea unui antet
    Primeste adresa in forma de string si numele antetului in forma de string """
    response = fetch(url)
    return response.headers.get(name, default) 

print(get_header(BASE_URL, name="Server"))

# Exercițiul 30
print("Exercițiul 30")
def security_headers(url):
    """ Verifica prezenta si returneaza aceste antete de securitate 
    Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
    Primeste adresa in forma de string """
    check = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    rez = {}
    response = fetch(url)
    for x in check:
        if x in response.headers:
            rez[x] = True
        else:
            rez[x] = False
    return rez

print(security_headers(BASE_URL))

# Exercițiul 31
print("Exercițiul 31")
def score_headers(results):
    """ Returneaza numarul de antete de securitate care sunt prezente
    Primeste dictionarul din security_headers() """
    a = 0
    for x in results:
        if results[x]:
            a += 1
    return f"{a}/5"


print(score_headers(security_headers(BASE_URL)))    

# Exercițiul 32
print("Exercițiul 32")
def fetch_robots(base):
    """ Returneaza textul fisierului robots.txt
    Primeste adresa de baza in forma de string """
    response = fetch(base + "/robots.txt")
    if response.status_code == 200:
        return response.text
    return None

def disallowed_paths(robots_text):
    """ Returneaza o lista cu toatre valorile Disallow
    Primeste textul string returnat de fetch_robots """
    rez = []
    if robots_text == None:
         return rez
    for x in robots_text.splitlines():
        if "Disallow:" in x:
            rez.append(x.replace("Disallow:", "").strip())
    return rez

print(disallowed_paths(fetch_robots(BASE_URL)))

# Exercițiul 33
print("Exercițiul 33")
def response_times(*urls):
    """ Returneaza un dictionar cu url si timpul de raspuns a lor
    Primeste mai multe adrese ain forma de string """
    rez = {}
    for x in urls:
        response = fetch(x)
        time.sleep(1)
        rez[x] = str(response.elapsed)
    return rez

print(response_times(BASE_URL, ECHO_URL))

# Exercițiul 34
print("Exercițiul 34")
def log(message, **details):
    """ returneaza mesajul si detaliile oferite
    Primeste mesajul in forma de string si mai multe detalii dub foma de un dictionar """
    rez = f"{message}"
    for x, y in details.items():
        rez += f" | {x}={y}"
    return rez
    
print(log("verificat", url=BASE_URL, status=200))
# Diferența dintre print() și return este că ce este returnat cu return poate fi folosit mai departe nu doar arătat la terminal