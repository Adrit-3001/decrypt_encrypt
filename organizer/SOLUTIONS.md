# Answer key (organizers only, don't hand this out)

| Level | What players change | Picture reveals |
|---|---|---|
| 1 | `KEY = "open" * 4` | Level 2's key is `the-vault-pin` + 3 digits, and every real picture starts with `HUNT` |
| 2 | `START = "the-vault-pin"` and `if first_block.startswith(b"HUNT"):` (PIN is 731) | Level 3 has no key; paint repeated blocks white, everything else black |
| 3 | Replace `result += block` with the if/else below | `FLAG: PENGUIN` |

```python
for block in blocks:
    if counts[block] > 1:
        result += WHITE
    else:
        result += BLACK
```

## Common snags

- **Level 1:** typing `"open"` gives "Your key is 4 characters long". Point them at the `"hi" * 3` trick.
- **Level 2:** `startswith("HUNT")` with a normal string fails because `first_block` is bytes. They need `b"HUNT"`. This is a good moment to explain text vs bytes.
- **Level 3:** writing `if counts[block] == 2:` also works.

To change keys, clues or the flag, edit the constants at the top of `make_puzzle.py` and run `python organizer/make_puzzle.py` from the `aes-image-hunt` folder.
