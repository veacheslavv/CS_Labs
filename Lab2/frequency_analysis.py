"""
Laboratory Work No. 2 - Cryptanalysis of monoalphabetic ciphers
Author: Veaceslav Morari, FAF-243

A small frequency-analysis tool (similar to the interactive-maths.com service):
  * counts the letters of a ciphertext and compares them with English frequencies;
  * lets the analyst guess substitutions step by step and shows the partly
    decrypted text (ciphertext letters in UPPER case, guessed letters in lower case);
  * recovers the full key and the final plaintext.

Usage:
  python frequency_analysis.py variant16_ciphertext.txt              # interactive mode
  python frequency_analysis.py variant16_ciphertext.txt --steps variant16_steps.txt
  python frequency_analysis.py variant16_ciphertext.txt --plot charts/
"""

import argparse
import os
import sys
from collections import Counter

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Table 2.2 - frequency of English letters, %.
ENGLISH_FREQ = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23, "G": 2.01,
    "H": 6.09, "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03, "M": 2.41, "N": 6.75,
    "O": 7.51, "P": 1.93, "Q": 0.09, "R": 5.99, "S": 6.33, "T": 9.06, "U": 2.76,
    "V": 0.98, "W": 2.36, "X": 0.15, "Y": 1.97, "Z": 0.07,
}


# ------------------------------------------------------------------ analysis

def letter_counts(text):
    """Number of occurrences of every letter A-Z (case-insensitive)."""
    counts = Counter(ch for ch in text.upper() if ch in ALPHABET)
    return {letter: counts.get(letter, 0) for letter in ALPHABET}


def sorted_by_frequency(counts):
    """Letters ordered from the most to the least frequent (ties alphabetically)."""
    return sorted(counts, key=lambda letter: (-counts[letter], letter))


def english_order():
    return sorted(ENGLISH_FREQ, key=lambda letter: -ENGLISH_FREQ[letter])


def partial_decrypt(text, mapping):
    """Replace guessed cipher letters by lower-case plaintext letters.

    Letters without a guess stay as UPPER-case ciphertext, exactly like in the
    example from the laboratory work. Other characters are not encrypted.
    """
    result = []
    for ch in text.upper():
        result.append(mapping.get(ch, ch) if ch in ALPHABET else ch)
    return "".join(result)


def full_decrypt(text, mapping):
    """Decrypt keeping the original upper/lower case of the ciphertext."""
    result = []
    for ch in text:
        upper = ch.upper()
        if upper in mapping:
            plain = mapping[upper]
            result.append(plain.upper() if ch.isupper() else plain)
        else:
            result.append(ch)
    return "".join(result)


def recover_key(mapping):
    """Plaintext alphabet a..z -> ciphertext letter (Table 2.5 in the lab)."""
    inverse = {plain: cipher for cipher, plain in mapping.items()}
    return {plain: inverse.get(plain, "?") for plain in ALPHABET.lower()}


def add_substitution(mapping, cipher, plain):
    """Add the guess cipher -> plain. Returns an error message or None."""
    cipher, plain = cipher.upper(), plain.lower()
    if cipher not in ALPHABET or len(plain) != 1 or not plain.isalpha():
        return "a substitution looks like W=t (one cipher letter = one plain letter)"
    for other_cipher, other_plain in mapping.items():
        if other_plain == plain and other_cipher != cipher:
            return f"'{plain}' is already the image of {other_cipher}; remove it first (-{other_cipher})"
    mapping[cipher] = plain
    return None


# ------------------------------------------------------------------ printing

def print_frequency_tables(counts):
    total = sum(counts.values())
    print(f"Total letters: {total}\n")
    print("Letter frequencies (alphabetical):")
    print("  Letter " + " ".join(f"{c:>4}" for c in ALPHABET))
    print("  Count  " + " ".join(f"{counts[c]:>4}" for c in ALPHABET))
    print("\nLetter frequencies (descending):")
    order = sorted_by_frequency(counts)
    print("  Letter " + " ".join(f"{c:>4}" for c in order))
    print("  Count  " + " ".join(f"{counts[c]:>4}" for c in order))
    print("  %      " + " ".join(f"{100 * counts[c] / total:>4.1f}" for c in order))
    print("  English " + " ".join(f"{c:>4}" for c in english_order()))
    print()


def print_key(mapping):
    key = recover_key(mapping)
    print("Recovered key:")
    print("  Plaintext  " + " ".join(key))
    print("  Ciphertext " + " ".join(key[p] for p in key))


def print_wrapped(text, width=95, limit=None):
    words, line, lines = text.split(" "), "", []
    for word in words:
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}" if line else word
    lines.append(line)
    for out in lines[:limit]:
        print("  " + out)
    if limit and len(lines) > limit:
        print("  ...")


# ------------------------------------------------------------------ charts

def save_charts(counts, folder):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(folder, exist_ok=True)
    charts = [
        ("english_frequencies.png", "Frequency of English letters (Table 2.2)",
         [ENGLISH_FREQ[c] for c in ALPHABET], "Frequency, %"),
        ("ciphertext_frequencies.png", "Frequency of letters in the intercepted ciphertext (V16)",
         [counts[c] for c in ALPHABET], "Number of occurrences"),
    ]
    for name, title, values, ylabel in charts:
        fig, ax = plt.subplots(figsize=(8, 3.2), dpi=200)
        ax.bar(list(ALPHABET), values, width=0.6, color="#2a78d6", zorder=3)
        ax.set_title(title, fontsize=11, color="#0b0b0b")
        ax.set_xlabel("Letters", color="#52514e")
        ax.set_ylabel(ylabel, color="#52514e")
        ax.grid(axis="y", color="#e4e3df", linewidth=0.8, zorder=0)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#b9b8b3")
        ax.tick_params(colors="#52514e", labelsize=9)
        ax.margins(x=0.01)
        fig.tight_layout()
        fig.savefig(os.path.join(folder, name))
        plt.close(fig)
        print(f"Saved {os.path.join(folder, name)}")


# ------------------------------------------------------------------ modes

def read_steps(path):
    """Each non-empty line: 'V=e W=t  # comment'. Returns [(comment, pairs)]."""
    steps = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            body, _, comment = line.partition("#")
            pairs = [p.split("=") for p in body.split()]
            if pairs:
                steps.append((comment.strip(), pairs))
    return steps


def run_steps(text, steps_path, preview_lines):
    mapping = {}
    for number, (comment, pairs) in enumerate(read_steps(steps_path), start=1):
        for cipher, plain in pairs:
            error = add_substitution(mapping, cipher, plain)
            if error:
                sys.exit(f"Step {number}: {error}")
        guesses = ", ".join(f"{c.upper()}->{p.lower()}" for c, p in pairs)
        print(f"Step {number}: {guesses}   ({comment})")
        print_wrapped(partial_decrypt(text, mapping), limit=preview_lines)
        print()
    return mapping


def run_interactive(text, preview_lines):
    mapping = {}
    print("Commands: W=t (add guess), -W (remove), show, freq, key, done\n")
    print_wrapped(partial_decrypt(text, mapping), limit=preview_lines)
    while True:
        command = input("\n> ").strip()
        if command == "done":
            return mapping
        if command == "show":
            print_wrapped(partial_decrypt(text, mapping))
        elif command == "freq":
            print_frequency_tables(letter_counts(text))
        elif command == "key":
            print_key(mapping)
        elif command.startswith("-") and len(command) == 2:
            mapping.pop(command[1].upper(), None)
            print_wrapped(partial_decrypt(text, mapping), limit=preview_lines)
        elif "=" in command:
            errors = [add_substitution(mapping, *pair.split("=", 1)) for pair in command.split()]
            for error in filter(None, errors):
                print(f"  Error: {error}")
            print_wrapped(partial_decrypt(text, mapping), limit=preview_lines)
        else:
            print("  Unknown command. Use W=t, -W, show, freq, key or done.")


def main():
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Frequency analysis of a monoalphabetic cipher")
    parser.add_argument("ciphertext", help="file with the intercepted ciphertext")
    parser.add_argument("--steps", help="file with the substitution steps to replay")
    parser.add_argument("--plot", metavar="FOLDER", help="save frequency charts to FOLDER")
    parser.add_argument("--preview", type=int, default=6, help="lines of text shown after each step")
    args = parser.parse_args()

    with open(args.ciphertext, encoding="utf-8") as f:
        text = f.read().strip()

    counts = letter_counts(text)
    print_frequency_tables(counts)
    if args.plot:
        save_charts(counts, args.plot)

    if args.steps:
        mapping = run_steps(text, args.steps, args.preview)
    else:
        mapping = run_interactive(text, args.preview)

    print_key(mapping)
    missing = [c for c in ALPHABET if counts[c] and c not in mapping]
    if missing:
        print(f"\nCipher letters without a guess: {' '.join(missing)}")
    print("\nDecrypted text:")
    print_wrapped(full_decrypt(text, mapping))


if __name__ == "__main__":
    main()
