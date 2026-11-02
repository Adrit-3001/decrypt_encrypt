# Level 2: crack the vault!
#
# vault.png is locked with the key "the-vault-pin" + a 3-digit PIN we don't know.
# 000 to 999 is only 1000 guesses. Too boring for a human, easy for a loop.
#
# But how does the computer know when a guess is right? Every hidden picture
# in this hunt starts with the bytes "HUNT". Real files do this too: every PNG
# starts with "\x89PNG" and every PDF with "%PDF". It's called a "magic number".
#
# Run it:    python crack_the_pin.py

from PIL import Image
from Crypto.Cipher import AES

picture = Image.open("vault.png")
scrambled = picture.tobytes()

for pin in range(1000):                            # pin = 0, 1, 2, ... 999
    key = "the-vault-pin" + str(pin).zfill(3)      # zfill pads with zeros: 7 -> "007"
    aes = AES.new(key.encode(), AES.MODE_ECB)
    first_block = aes.decrypt(scrambled[:16])      # just the first 16 bytes, so each guess is instant

    if False:  # YOUR TURN: replace False with a check that first_block starts with b"HUNT"
        print("Cracked it! The key is", key)
        break

# Unlock the whole picture with the key the loop stopped on
aes = AES.new(key.encode(), AES.MODE_ECB)
Image.frombytes("RGB", picture.size, aes.decrypt(scrambled)).save("vault_open.png")
print("Open vault_open.png")
