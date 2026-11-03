# AES Image Hunt

Three pictures, each locked with encryption. Each one you unlock holds the clue for the next.

## Play in the browser (nothing to install)

The `web/` folder is the whole game as a website. Python runs inside the browser.

- **Try it locally:** `cd web && python -m http.server 8000`, then open http://localhost:8000
  (opening `index.html` directly won't work: browsers block it from loading the puzzle files)
- **Put it online (one-time setup):** GitHub repo → Settings → Pages → Source: **GitHub Actions**.
  Every push to `main` then publishes the `web/` folder to `https://<user>.github.io/<repo>/`

## Play in the terminal

Install the two helpers (once):  `pip install pillow pycryptodome`

| Level | Open this file | Then run | Then look at |
|---|---|---|---|
| 1 | `level1_decrypt.py` | `python level1_decrypt.py` | `level1_open.png` |
| 2 | `level2_crack_pin.py` | `python level2_crack_pin.py` | `level2_open.png` |
| 3 | `level3_find_patterns.py` | `python level3_find_patterns.py` | `level3_open.png` |

In each file, change the lines marked `YOUR TURN`. The first person to find the final flag wins!
