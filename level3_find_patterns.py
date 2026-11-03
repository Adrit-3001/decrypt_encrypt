# Level 3: no key? No problem.
#
# level3.png uses a key nobody knows. But it was encrypted with AES in "ECB" mode,
# which scrambles the picture in separate 16-byte chunks called blocks.
# The picture from level 2 tells you ECB's weakness. Use it to find the final flag.
#
# Run it:    python level3_find_patterns.py

from collections import Counter
from PIL import Image

picture = Image.open("level3.png")
scrambled = picture.tobytes()

blocks = [scrambled[i:i + 16] for i in range(0, len(scrambled), 16)]   # chop into 16-byte blocks
counts = Counter(blocks)   # counts[block] = how many times that exact block appears in the picture

WHITE = b"\xff" * 16       # 16 bytes of 255 = a white strip of pixels
BLACK = b"\x00" * 16       # 16 bytes of 0   = a black strip of pixels

result = bytearray()
for block in blocks:
    result += block        # YOUR TURN: add WHITE or BLACK instead, depending on counts[block]

Image.frombytes("RGB", picture.size, bytes(result)).save("level3_open.png")
print("Open level3_open.png")
