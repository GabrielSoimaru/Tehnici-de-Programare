from PIL import Image
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj)
# TODO: pentru fiecare bit, ia un canal si pune
# canal = (canal & ~1) | int(bit)
# TODO: img.putdata(px_nou); img.save("stego.png")
canale = [c for pixel in px for c in pixel]
for i, bit in enumerate(biti):
    canale[i] = (canale[i] & ~1) | int(bit)

px_nou = [tuple(canale[i:i+3]) for i in range(0, len(canale), 3)]
img.putdata(px_nou)
img.save("stego.png")

px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""
for (r, g, b) in px:
# TODO: aduna ultimii biti (r&1, g&1, b&1)
    biti += str(r & 1) + str(g & 1) + str(b & 1)
# TODO: grupeaza cate 8 biti -> octeti -> text
# opreste-te la primul octet 0 (final de mesaj)
mesaj = b""
for i in range(0, len(biti), 8):
    octet = int(biti[i:i+8], 2)
    if octet == 0:
        break
    if not 32 <= octet < 127:
        break
    mesaj += bytes([octet])
print(mesaj.decode())