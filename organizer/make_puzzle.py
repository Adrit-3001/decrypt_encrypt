# Organizer only: builds the encrypted puzzle images. Participants never need this file.
#
# Run from the aes-image-hunt folder:    python organizer/make_puzzle.py
#
# Each picture holds the clue for the next level:
#   level1.png  key given away by the hint in level1_decrypt.py
#   level2.png  key brute-forced using the clue in level 1's picture
#   level3.png  no key at all, cracked by spotting ECB's repeated blocks

import random

from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES

LEVEL1_KEY = "open" * 4
LEVEL1_LINES = ["LEVEL 1 DONE!", "",
                "Level 2's key is", "the-vault-pin + 3 digits",
                "",
                "Every real picture here", "starts with the bytes HUNT"]

LEVEL2_KEY = "the-vault-pin731"
LEVEL2_LINES = ["VAULT OPEN!", "",
                "Level 3 has no key, but", "ECB has a weakness:",
                "same block in = same block out", "",
                "Paint repeated blocks white,", "everything else black"]

LEVEL3_KEY = "nobody-knows-me!"  # never given to players
LEVEL3_LINES = ["YOU WIN!", "FLAG:", "PENGUIN"]

SIZE = 480  # 480 * 480 * 3 bytes is a multiple of 16, which AES needs
MAGIC = b"HUNT"  # hidden pictures start with these bytes, so players' code can recognise success


def load_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default(size)


def gradient_background():
    red = Image.linear_gradient("L").rotate(90).resize((SIZE, SIZE))
    green = Image.radial_gradient("L").resize((SIZE, SIZE))
    blue = Image.new("L", (SIZE, SIZE), 170)
    return Image.merge("RGB", (red, green, blue))


def draw_lines(image, lines, max_font_size, **style):
    draw = ImageDraw.Draw(image)
    # Shrink the font until the widest line fits
    for font_size in range(max_font_size, 10, -2):
        font = load_font(font_size)
        if all(draw.textlength(line, font=font) <= SIZE - 40 for line in lines):
            break
    line_height = int(font_size * 1.35)
    y = (SIZE - line_height * (len(lines) - 1)) // 2
    for line in lines:
        draw.text((SIZE // 2, y), line, font=font, anchor="mm", **style)
        y += line_height


def add_faint_noise(image):
    # ECB encrypts identical 16-byte blocks to identical output, so flat areas
    # would show through the ciphertext. A tiny random wobble makes every block
    # unique; it's invisible after decryption.
    rng = random.Random(27)
    pixels = bytes(min(255, max(0, p + rng.randint(-3, 3))) for p in image.tobytes())
    return Image.frombytes("RGB", image.size, pixels)


def keyed_picture(lines):
    image = gradient_background()
    draw_lines(image, lines, 44, fill="white", stroke_width=3, stroke_fill="black")
    pixels = add_faint_noise(image).tobytes()
    # The magic bytes only recolour the first pixel or two, which nobody will notice
    return MAGIC + pixels[len(MAGIC):]


def pattern_picture(lines):
    # Real ECB leaks come from flat colours, but flat text shows through the
    # ciphertext so clearly that nobody would need code. Instead, each text block
    # gets random bytes shared with exactly one other text block: the ciphertext
    # looks like pure static, yet counting repeated blocks still reveals the text.
    pixels = bytearray(add_faint_noise(gradient_background()).tobytes())
    mask = Image.new("RGB", (SIZE, SIZE), "black")
    draw_lines(mask, lines, 90, fill="white")
    mask_bytes = mask.tobytes()
    text_blocks = [i for i in range(0, len(pixels), 16) if mask_bytes[i:i + 16].count(255) >= 8]

    rng = random.Random(3)
    rng.shuffle(text_blocks)
    for n in range(0, len(text_blocks) - 1, 2):
        shared = rng.randbytes(16)
        for i in text_blocks[n:n + 2]:
            pixels[i:i + 16] = shared
    return bytes(pixels)


def save_encrypted(output, key, pixels):
    scrambled = AES.new(key.encode(), AES.MODE_ECB).encrypt(pixels)
    Image.frombytes("RGB", (SIZE, SIZE), scrambled).save(output)
    print(f"Wrote {output} (key: {key})")


if __name__ == "__main__":
    save_encrypted("level1.png", LEVEL1_KEY, keyed_picture(LEVEL1_LINES))
    save_encrypted("level2.png", LEVEL2_KEY, keyed_picture(LEVEL2_LINES))
    save_encrypted("level3.png", LEVEL3_KEY, pattern_picture(LEVEL3_LINES))
