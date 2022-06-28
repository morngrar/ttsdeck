#!/usr/bin/python3

import sys
from PIL import Image
import os

def get_image(path):
    img = Image.open(path)
    img.load()
    img.resize((312, 445), Image.Resampling.LANCZOS)

    return img


def main():

    if len(sys.argv) != 2:
        print(f"Supply dir with images. The back image must be named 'back.jpg'")
        return

    image_dir = sys.argv[1]
    back_path = os.path.join(image_dir, "back.jpg")

    background = Image.new("RGB", (3320, 3255), "black")

    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
    images = filter(lambda f: os.path.isfile(f), images)

    pos = 0
    for image in images:
        if image == back_path or image[-4:] != ".jpg":
            continue
        img = get_image(image)
        background.paste(img, (pos % 10 * 332 + 10, int(pos / 10) * 465 + 10))
        pos += 1


    print("[+] Loading Card Back...")
    img = get_image(back_path)
    background.paste(img, (9 * 332 + 10, 6 * 465 + 10))

    print("[+] Saving")
    background.save("deck.jpg", "JPEG")


if __name__ == "__main__":
    main()
