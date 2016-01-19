#!/usr/bin/env python3

import html
import re
import sys
import urllib.request

from PIL import Image
from io import BytesIO

def load_deck(deck):
    main = {}
    side = {}

    with open(deck) as f:
        data = f.read()

    in_sideboard = False
    for line in data.split('\n'):
        if not line.strip():
            in_sideboard = True
            continue

        exp = re.search("([0-9]+) (.+)", line.strip())
        amount = exp.group(1)
        card = exp.group(2)

        if not in_sideboard:
            main[card] = amount
        else:
            side[card] = amount

    return main, side

def get_image(card):
    url = "http://magiccards.info/query?{}".format(urllib.parse.urlencode({'q':card}))

    with urllib.request.urlopen(url) as f:
        data = f.read().decode('utf-8')

    data = html.unescape(data)

    p = re.compile('<img src="([^"]+)"\s$', re.M)
    m = p.search(data)

    with urllib.request.urlopen(m.group(1)) as f:
        data = f.read()

    img = Image.open(BytesIO(data))
    img.load()
    img.resize((312, 445), Image.ANTIALIAS)

    return img

def get_back():
    url = "https://upload.wikimedia.org/wikipedia/en/a/aa/Magic_the_gathering-card_back.jpg"

    with urllib.request.urlopen(url) as f:
        data = f.read()

    img = Image.open(BytesIO(data))
    img.load()
    img.resize((312, 445), Image.ANTIALIAS)

    return img

def main():
    if len(sys.argv) != 2:
        print("{} decklist".format(sys.argv[0]))
        return

    main, side = load_deck(sys.argv[1])

    background = Image.new("RGBA", (3320, 3255), "black")

    pos = 0
    for key, value in main.items():
        print("[+] Loading: {}x {}".format(value, key))
        img = get_image(key)
        for i in range(int(value)):
            background.paste(img, (pos % 10 * 332 + 10, int(pos / 10) * 465 + 10))
            pos += 1


    print("[+] Loading Card Back...".format(value, key))
    img = get_back()
    background.paste(img, (9 * 332 + 10, 6 * 465 + 10))

    print("[+] Saving")
    background.save("deck.jpg", "JPEG")


if __name__ == "__main__":
    main()
