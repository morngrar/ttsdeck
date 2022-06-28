#!/usr/bin/python3

import sys
from PIL import Image
import os

img_width = 300*10
img_height = 419*7

slot_width = img_width // 10 #332
slot_height = img_height // 7 #465

row_len = 10
card_width = slot_width * 1 #312
card_height = slot_height * 1#445
 
def get_image(path):
    img = Image.open(path)
    img.load()

    width_percent = (card_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))
    img = img.resize((card_width, height_size), Image.Resampling.NEAREST)

    return img


def main():

    if len(sys.argv) != 2:
        print(f"Supply dir with images. The back image must be named 'back.jpg'")
        return

    image_dir = sys.argv[1]
    back_path = os.path.join(image_dir, "back.jpg")

    background = Image.new("RGB", (img_width, img_height), "black")

    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
    images = filter(lambda f: os.path.isfile(f), images)

    pos = 0
    for image in images:
        if image == back_path or image[-4:] != ".jpg":
            continue
        img = get_image(image)
        background.paste(
            img, 
            (
                (pos % row_len) * slot_width, #+ row_len, 
                pos // row_len * slot_height #+ row_len
            )
        )
        pos += 1


    print("[+] Loading Card Back...")
    img = get_image(back_path)
    background.paste(img, (9 * slot_width, 6 * slot_height ))

    print("[+] Saving")
    background.save(os.path.join(image_dir, "deck.jpg"), "JPEG")


if __name__ == "__main__":
    main()
