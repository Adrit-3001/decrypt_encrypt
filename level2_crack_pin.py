# Level 2: crack the vault!
#
# level2.png is locked with a key that ends in a PIN we don't know.
# Guessing by hand would take forever, but a loop can try every PIN in a blink.
# The picture from level 1 tells you what the key looks like.
#
# Run it:    python level2_crack_pin.py

from PIL import Image
from Crypto.Cipher import AES

picture = Image.open("level2.png")
scrambled = picture.tobytes()

START = "?"   # YOUR TURN: what does every vault key start with? (see level 1's picture)

if len(START) + 3 != 16:
    raise SystemExit(f"START + 3 digits must be 16 characters, but START is {len(START)} long.")

for pin in range(1000):                            # pin = 0, 1, 2, ... 999
    key = START + str(pin).zfill(3)                # zfill pads with zeros: 7 -> "007"
    aes = AES.new(key.encode(), AES.MODE_ECB)
    first_block = aes.decrypt(scrambled[:16])      # just the first 16 bytes, so each guess is instant

    if False:  # YOUR TURN: replace False with a check on first_block. Tip: "hello".startswith("he")
        print("Cracked it! The key is", key)
        break
else:
    raise SystemExit("No PIN worked. Check START and your check, then try again.")

# Unlock the whole picture with the key the loop stopped on
aes = AES.new(key.encode(), AES.MODE_ECB)
Image.frombytes("RGB", picture.size, aes.decrypt(scrambled)).save("level2_open.png")
print("Open level2_open.png")
