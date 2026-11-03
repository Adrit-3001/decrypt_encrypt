# Level 1: unlock the first picture
#
# level1.png was scrambled with AES, the same encryption that protects
# your banking app and your messages. With the right key, we can unscramble it.
#
# HINT: The magic word is "open". But AES is picky: keys must be EXACTLY
#       16 characters long. Python trick:  "hi" * 3  gives  "hihihi"
#
# Run it:    python level1_decrypt.py
# Then open level1_open.png. The picture tells you how to beat level 2.

from PIL import Image          # opens and saves pictures
from Crypto.Cipher import AES  # the AES encryption algorithm

KEY = "?"                      # YOUR TURN: use the hint to build the key

if len(KEY) != 16:
    raise SystemExit(f"Your key is {len(KEY)} characters long, but AES needs exactly 16.")

picture = Image.open("level1.png")
scrambled = picture.tobytes()                 # the picture as one long list of numbers (bytes)

aes = AES.new(KEY.encode(), AES.MODE_ECB)
unscrambled = aes.decrypt(scrambled)          # AES turns the numbers back into the originals

Image.frombytes("RGB", picture.size, unscrambled).save("level1_open.png")
print("Done! Open level1_open.png")
