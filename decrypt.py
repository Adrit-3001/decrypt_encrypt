# Decrypt the mystery image!
#
# mystery.png was scrambled with AES, the same encryption that protects
# your banking app and your messages. With the right key, we can unscramble it.
#
# Run it:    python decrypt.py
# Then open revealed.png to see what was hidden.

from PIL import Image          # opens and saves pictures
from Crypto.Cipher import AES  # the AES encryption algorithm

KEY = "sixteen-letterz!"       # AES keys are exactly 16 characters. Try changing one letter!

picture = Image.open("mystery.png")
scrambled = picture.tobytes()                 # the picture as one long list of numbers (bytes)

aes = AES.new(KEY.encode(), AES.MODE_ECB)
unscrambled = aes.decrypt(scrambled)          # AES turns the numbers back into the originals

Image.frombytes("RGB", picture.size, unscrambled).save("revealed.png")
print("Done! Open revealed.png")
