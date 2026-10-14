# Laborator: funcții, metode și importuri pe web
# Student: Șoimaru Gabriel
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 3  # secunde

# Exercițiul 44
print("Exercițiul 44")
import webtools
print(webtools.get_title(webtools.fetch(BASE_URL).text))

# Exercițiul 45
from webtools import get_title, security_headers
# Daca main.py ar avea propria functie numita get_title, functia definita sau importata ultima se va suprascrie peste prima 

# Exercițiul 46
# Acel loc verifica daca fisierul curent este fisierul original al blocului sau doar importat de undeva

# Exercițiul 47
print("Exercițiul 47")
print(webtools.DEFAULT_HEADERS)


# Exercițiul 48
""" print("Exercițiul 48")
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("url")
argumente = parser.parse_args()
BASE_URL = argumente.url """

""" print(webtools.get_status(BASE_URL)) """


# Exercițiul 49
print("Exercițiul 49")
import csv
import datetime
paths = webtools.check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"])
with open ("report.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["path", "status", "checked_at"])
    for path, status in paths.items():
        timp = datetime.datetime.now().isoformat()
        writer.writerow([path, status, timp])

# Exercițiul 50
print("Exercițiul 50")
webtools.site_report(BASE_URL)