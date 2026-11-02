# Organizer only: builds the encrypted puzzle images. Participants never need this file.
#
# Run from the aes-image-hunt folder:    python organizer/make_puzzle.py

import random

from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES

# (output file, key, lines of text drawn on the hidden picture)
PUZZLES = [
    ("mystery.png", "sixteen-letters!",
     ["YOU CRACKED IT!", "", "clue #1:", "the vault PIN", "has 3 digits"]),
    ("vault.png", "the-vault-pin731",
     ["VAULT OPEN!", "", "clue #2:", "ECB can't keep", "secrets..."]),
]
SIZE = 480  # 480 * 480 * 3 bytes is a multiple of 16, which AES needs
MAGIC = b"HUNT"  # every hidden picture starts with these bytes, so players' code can recognise success


def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default(size)


def draw_clue(lines):
    # Smooth colour gradient background, so the decrypted picture looks clearly "real"
    red = Image.linear_gradient("L").rotate(90).resize((SIZE, SIZE))
    green = Image.radial_gradient("L").resize((SIZE, SIZE))
    blue = Image.new("L", (SIZE, SIZE), 170)
    image = Image.merge("RGB", (red, green, blue))

    draw = ImageDraw.Draw(image)
    font = load_font(40)
    y = 110
    for line in lines:
        draw.text((SIZE // 2, y), line, font=font, fill="white", anchor="mm",
                  stroke_width=3, stroke_fill="black")
        y += 55
    return image


def add_faint_noise(pixels):
    # ECB encrypts identical 16-byte blocks to identical output, so flat areas
    # (like solid text) would show through the ciphertext. A tiny random wobble
    # makes every block unique; it's invisible after decryption.
    rng = random.Random(27)
    return bytes(min(255, max(0, p + rng.randint(-3, 3))) for p in pixels)


if __name__ == "__main__":
    for output, key, lines in PUZZLES:
        clue = draw_clue(lines)
        # The magic bytes only recolour the first pixel or two, which nobody will notice
        pixels = MAGIC + add_faint_noise(clue.tobytes())[len(MAGIC):]
        scrambled = AES.new(key.encode(), AES.MODE_ECB).encrypt(pixels)
        Image.frombytes("RGB", clue.size, scrambled).save(output)
        print(f"Wrote {output} (key: {key})")
