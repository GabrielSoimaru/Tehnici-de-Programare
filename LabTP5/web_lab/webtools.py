# Laborator: funcții, metode și importuri pe web
# Student: Șoimaru Gabriel
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 3  # secunde
DEFAULT_HEADERS = {"User-Agent": "WebLab-Soimaru Gabriel"}

import requests
import time
import socket
import datetime
import ssl
import urllib.parse
import re
import json

def fetch(url):
    """ Returneaza obiectul raspuns dupa .get
    Primeste adresa in forma de string """
    response = requests.get(url, timeout=TIMEOUT, headers=DEFAULT_HEADERS)
    return response

def get_status(url): 
   """ Returneaza codul de stare a obiectului raspuns dupa .get
   Primeste adresa in forma de string """
   response = requests.get(url, timeout=TIMEOUT)
   return response.status_code

def get_title(html):
    """ Returneaza titlul fisierului html introdus
    Primeste fisierul html (textul din raspunsul de dupa .get) """
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

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

def check_paths(base, paths):
    """ Returneaza nu dictionar format din linkul de baza si stringurile din lista primita
    Primeste adresa in forma string si o lista cu stringuri """
    rez = {}
    for x in paths:
        y = get_status(base + x)
        time.sleep(1)
        rez[base + x] = y
    return rez

def resolve(hostname):
    """ Returneaza adresa ip a unui site 
    Primeste numele site-ului in forma de string """
    ip = socket.gethostbyname(hostname)
    return ip

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

def score_headers(results):
    """ Returneaza numarul de antete de securitate care sunt prezente
    Primeste dictionarul din security_headers() """
    a = 0
    for x in results:
        if results[x]:
            a += 1
    return f"{a}/5"

def cert_days_left(hostname):
    """ Verifica certificatul https a unui site si returneaza cate zile mia sunt pana expira
    Primeste numele site-ului in forma de string """
    context = ssl.create_default_context()
    sock = socket.create_connection((hostname, 443))
    con = context.wrap_socket(sock, server_hostname=hostname)
    cert = con.getpeercert()["notAfter"]
    seconds = ssl.cert_time_to_seconds(cert)
    data = datetime.datetime.fromtimestamp(seconds)
    prezent = datetime.datetime.now()
    rez = data - prezent
    return rez.days

def extract_links(html):
    """ Returneaza toate legaturile/linkuri fara duplicate
    Primesete textul fisierului html ca string """
    rez = re.findall(r'href="([^"]+)"', html)
    return set(rez)

def split_links(links, domain):
    """ Returneaza doua liste: linkurile interne si cele externe 
    Primeste lista sau setul de linkuri obtinute din extract_links si adresa de baza a site-ului in forma de string """
    intern = []
    extern = []
    loc1 = urllib.parse.urlparse(domain).netloc
    for x in links:
        link = urllib.parse.urljoin(domain, x)
        loc2 = urllib.parse.urlparse(link).netloc
        if loc1 == loc2:
            intern.append(link)
        else:
            extern.append(link)
    return intern, extern

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

def redirect(url):
    response = fetch(url)
    lis = []
    for x in response.history:
        lis.append(str(x.status_code))
        lis.append(str(response.url))
    rez = " -> ".join(lis)
    return rez

def site_report(url):
    response = fetch(url)   
    domeniu = urllib.parse.urlparse(url).netloc
    site = response.url
    code = get_status(url)
    title = get_title(response.text)
    ip = resolve(domeniu)
    redirectionari = redirect("http://" + domeniu)
    scor_sec = score_headers(security_headers(url))
    cert = cert_days_left(domeniu)
    links = split_links(extract_links(response.text), url)
    robots_paths = disallowed_paths(fetch_robots(url))

    raport = {
        "Raport site": site,
        "Cod de stare": code,
        "Titlu": title,
        "Adresa IP": ip,
        "Redirectionari": redirectionari,
        "Scor securitate": scor_sec,
        "Certificat": str(cert) + "de zile ramase",
        "Legaturi interne": len(links[0]), 
        "Legaturi externe": len(links[1]), 
        "Cai interzise": robots_paths
    }

    with open("report.json", 'w') as file:
        json.dump(raport, file, indent=4)

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))

