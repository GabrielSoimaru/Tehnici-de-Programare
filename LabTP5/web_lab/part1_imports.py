# Laborator: funcții, metode și importuri pe web
# Student: Șoimaru Gabriel
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 3  # secunde

import time

# Exercițiul 1
print("Exercițiul 1")
import requests
print(requests.__version__)
import urllib.request
# request a avut nevoie de pip install deoarcee nu este o bibliotecă default python, în timp ce urllib este

# Exercițiul 2
print("Exercițiul 2")
print(requests.get(BASE_URL, timeout=TIMEOUT).status_code)
from requests import get
time.sleep(1)
print(get(BASE_URL, timeout=TIMEOUT).status_code)
# Avantajul primei metode este că dacă importăm toată biblioteca putem folosi toate funțiile din ea dacă avem nevoie mai încolo
# Avantajul metoddei doi este că dacă folosim doar .get() nu este nevoie să importăm toată biblioteca, astfel ușurând programul

time.sleep(1)

# Exercițiul 3
print("Exercițiul 3")
import requests as rq
rq.get(BASE_URL, timeout=TIMEOUT)
# Un alias face codul mai ușor atunci când vrei să dai import la o bibliotecă cu o denumire lungă și complicată, iar prin alias folosești o denumire mai scurtă
# Un alias face codul mai greu atunci când aliasul nu este destul de descriptiv și este greu de descifrat la ce bibliotecă se referă aliasul

time.sleep(1)

# Exercițiul 4 (Dacă pun BASE_URL dă status code 403)
print("Exercițiul 4")
response = urllib.request.urlopen(ECHO_URL, timeout=TIMEOUT)
print(response.status)
text = response.read()[:200]
print(text.decode("utf-8"))

# Exercițiul 5
print("Exercițiul 5")
print(dir(requests))
# get - funcție
# Response - clasă
# exceptions - modul

# Exercițiul 6
print("Exercițiul 6")
help(requests.get)
requests.get(BASE_URL, timeout=TIMEOUT)

time.sleep(1)

# Exercițiul 7
print("Exercițiul 7")
import time
start = time.perf_counter()
response = requests.get(BASE_URL, timeout=TIMEOUT)
end = time.perf_counter()
print(end - start)
print(response.elapsed)
# Comparație - time.perf_counter() este  puțin mai mare decât response.elapsed deoarece time.perf_counter măsoară timpul total de execuție a liniilor în timp ce response.elapsed măsoară doar timpul de răspuns a site-ului

# Exercițiul 8
print("Exercițiul 8")
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")

# Diferența dintre un modul, un pachet și o bibliotecă
# Un modul este un singur fișier .py care conține care conține cod Python precum funcții, clase și variabile
# Un pachet este un folder care conține mai multe module
# O bibliotecă este un o colecție mai mare de module și pachete