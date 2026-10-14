# Laborator: funcții, metode și importuri pe web
# Student: Șoimaru Gabriel
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 3  # secunde

import requests
import time
import urllib.parse
import re

# Exercițiul 35
print("Exercițiul 35")
def parse(url):
    """ Returneza .scheme, .netloc, .path, .query si .fragment pt adresa propusa
    Primese o adresa in forma de string """
    response = urllib.parse.urlparse(url)
    return response.scheme, response.netloc, response.path, response.query, response.fragment

print(parse("https://cybercor.org/path?x=1#top"))    

# Exercițiul 36
print("Exercițiul 36")
def join(*ends):
    """ Returneaza unirea dintre adresa de baza si o lista de terminatii prin .urljoin
    Primeste mai multe stringuri """
    rez = []
    for x in ends:
        rez.append(urllib.parse.urljoin(BASE_URL, x))
    return rez

print(join("/about", "contact.html", "../index.html"))   

# Exercițiul 37
print("Exercițiul 37")
def extract_links(html):
    """ Returneaza toate legaturile/linkuri fara duplicate
    Primesete textul fisierului html ca string """
    rez = re.findall(r'href="([^"]+)"', html)
    return set(rez)

html_text = requests.get(BASE_URL, timeout=TIMEOUT).text
print(extract_links(html_text))

# Exercițiul 38
print("Exercițiul 38")
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

interne, externe = split_links(extract_links(html_text), BASE_URL)
print("Linkuri interne: ", interne)
print("Linkuri externe: ", externe)

# Exercițiul 39
print("Exercițiul 39")
from html.parser import HTMLParser

class ImageFinder(HTMLParser):
    def __init__(self):
        """ Intializeaza clasa curenta si mosteneste caracteristicile clasei parinte HTMLParser  
        Si declara lista .images"""
        super().__init__()
        self.images = []
    
    def handle_starttag(self, tag, attrs):
        """ Colecteaza atributul src a fiecarui tag img si le adauga la lista self.images 
        Primeste tag-ul si attributele automat """
        if tag.lower() == "img":
            sursa = dict(attrs).get("src")
            if sursa:
                self.images.append(sursa)


test_html = """
<html><body>
    <img src="/logo.png" alt="Logo">
    <IMG SRC="poza.jpg">
    <img alt="imagine fără src">
    <img src="https://cdn.example.com/banner.webp" />
    <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png", # imagine obișnuită
    "poza.jpg", # tag scris cu majuscule
    "https://cdn.example.com/banner.webp", # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")

response = requests.get(BASE_URL, timeout=TIMEOUT)
finder = ImageFinder()
finder.feed(response.text)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)
        
print(response.text.lower().count("<img"))

time.sleep(1)

# Exercițiul 40
print("Exercițiul 40")
import hashlib
def page_fingerprint(url):
    """ Foloesete sha256 pentru a face hash la continutul fisierului html 
    Primeste adresa in forma de string"""
    response = requests.get(url)
    rez = hashlib.sha256(response.content).hexdigest()
    return rez

print(page_fingerprint(BASE_URL))
print(page_fingerprint(BASE_URL))
# Rezultatele sunt identice. 
# Rezultatele vor fi diferite atunci cand continutul fisierului html a siteului din a doua rulare difera de prima, astfel prin hashing rezultatul va fi diferit

time.sleep(1)

# Exercițiul 41
print("Exercițiul 41")
import json
def html_json(url, fisier):
    """ Salveaza, citeste si returneaza antetele fisierului html in format json
    Primeste adresa in forma de string si un string cu numele fisierului dorit """
    response = requests.get(url)
    with open(fisier, 'w') as file:
        json.dump(dict(response.headers), file, indent=2)
    with open(fisier, 'r') as file:
        rez = json.load(file)
    return rez.get("Date")

print(html_json(BASE_URL, "headers.json"))

time.sleep(1)

# Exercițiul 42
print("Exercițiul 42")
import socket
def resolve(hostname):
    """ Returneaza adresa ip a unui site 
    Primeste numele site-ului in forma de string """
    ip = socket.gethostbyname(hostname)
    return ip

print(resolve("cybercor.org"))

time.sleep(1)

# Exercițiul 43
print("Exercițiul 43")
import ssl
import datetime
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

print(cert_days_left("cybercor.org"), "zile")

#In exercițiul 39 handle_starttag() este apelat automat de metoda feed() din clasa HTMLParser