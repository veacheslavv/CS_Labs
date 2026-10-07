# Laboratory Work No. 2 — Cryptanalysis of Monoalphabetic Ciphers

**Course:** Cryptography and Security
**Author:** Veaceslav Morari, FAF-243
**Teacher:** Maia Zaica
**Variant:** 16

## Task

An English message encrypted with a monoalphabetic substitution cipher was intercepted (only the letters were encrypted). The task is to recover the plaintext and the key with a frequency analysis attack and to describe the breaking process step by step.

## Files

| File | Contents |
| --- | --- |
| `frequency_analysis.py` | Frequency analysis tool: letter counts, comparison with English, step-by-step substitutions, key recovery, charts |
| `test_frequency_analysis.py` | Unit tests |
| `variant16_ciphertext.txt` | The intercepted cryptogram (variant 16) |
| `variant16_steps.txt` | The substitutions made at each step, with the reason for each one |
| `charts/` | Letter frequency charts (English and ciphertext) |
| `screenshots/` | Screenshots of the running program used in the report |
| `report/Lab2_Report.pdf` | The laboratory report ([PDF](report/Lab2_Report.pdf), LaTeX source in `report/Lab2_Report.tex`) |

## How to run

Requires Python 3.7+ (and `matplotlib` only for `--plot`).

```
python frequency_analysis.py variant16_ciphertext.txt                               # interactive mode
python frequency_analysis.py variant16_ciphertext.txt --steps variant16_steps.txt   # replay the solution
python frequency_analysis.py variant16_ciphertext.txt --steps variant16_steps.txt --plot charts
python -m unittest -v test_frequency_analysis
```

Interactive commands: `W=t` (add a guess, several per line are allowed), `-W` (remove a guess), `show`, `freq`, `key`, `done`.

## Result

The plaintext is an excerpt about the telegraph and Thomas Jefferson's "wheel cypher". Recovered key:

| Plaintext | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ciphertext | T | A | H | O | V | C | J | Q | X | E | L | S | Z | G | N | U | B | I | P | W | D | K | R | Y | F | M |
