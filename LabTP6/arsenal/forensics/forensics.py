def tip_real(cale):
    cap = open(cale, "rb").read(8)
    # TODO: daca cap incepe cu b"%PDF" -> "pdf"
    # b"\x89PNG" -> "png" ; b"\xff\xd8" -> "jpeg"
    # b"PK\x03\x04" -> "zip/docx"
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()
print(tip_real("probe/foto.jpg"))

import re
date = open("probe/ascuns.png", "rb").read()
# TODO: for m in re.findall(rb"[ -~]{4,}", date):
# print(m.decode())
# cauta un indiciu: o cale, un mesaj, un nume de fisier
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

from PIL import Image
from PIL.ExifTags import TAGS
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)
# TODO: ia blocul GPS (tag 34853) si tipareste
# latitudinea si longitudinea
gps = exif.get(34853)
g, m, s = gps[2]
lat = g + m / 60 + s / 3600
g, m, s = gps[4]
lon = g + m / 60 + s / 3600
print("lat:", float(lat), "lon:", float(lon))

date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
# TODO: daca i != -1:
# open("gasit.zip","wb").write(date[i:])
# print("arhiva extrasa de la octetul", i)
# apoi dezarhiveaza si vezi ce era inauntru
if i != -1:
    open("gasit.zip","wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)
