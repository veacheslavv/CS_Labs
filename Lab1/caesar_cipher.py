"""
Laboratory Work No. 1 - The Caesar Cipher
Author: Veaceslav Morari, FAF-243

Task 1.1 - Caesar cipher over the Romanian alphabet (n = 31)
Task 1.2 - Caesar cipher with two keys (numeric shift + keyword permutation)
"""

import sys
import unicodedata

# Romanian alphabet in the order from Table 2 (A = 0, Ă = 1, ..., Z = 30).
ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "Ș", "T", "Ț", "U",
            "V", "W", "X", "Y", "Z"]
LOWERCASE = ["a", "ă", "â", "b", "c", "d", "e", "f", "g", "h", "i", "î", "j",
             "k", "l", "m", "n", "o", "p", "q", "r", "s", "ș", "t", "ț", "u",
             "v", "w", "x", "y", "z"]
N = len(ALPHABET)  # 31

# Letter -> code, built only from Table 2 (no ASCII / Unicode arithmetic).
CODE = {letter: i for i, letter in enumerate(ALPHABET)}

# Every accepted input character mapped to its uppercase Romanian letter.
# Ş/Ţ with a cedilla are accepted as Ș/Ț with a comma below.
TO_UPPER = {}
for upper, lower in zip(ALPHABET, LOWERCASE):
    TO_UPPER[upper] = upper
    TO_UPPER[lower] = upper
TO_UPPER.update({"Ş": "Ș", "ş": "Ș", "Ţ": "Ț", "ţ": "Ț"})

MIN_KEY, MAX_KEY = 1, N - 1
MIN_KEYWORD_LEN = 7


# ---------------------------------------------------------------- validation

def normalize_text(text):
    """Remove spaces and convert to uppercase Romanian letters.

    Returns (letters, None) on success or (None, bad_char) on the first
    character that is not a Romanian letter.
    """
    # NFC joins letters typed as base + combining mark (e.g. a + ˘ -> ă).
    text = unicodedata.normalize("NFC", text)
    result = []
    for ch in text:
        if ch == " ":
            continue
        if ch not in TO_UPPER:
            return None, ch
        result.append(TO_UPPER[ch])
    return "".join(result), None


def parse_key(raw):
    """Return the key as int if it is an integer in [1, 30], else None."""
    raw = raw.strip()
    if not raw.isdigit():
        return None
    key = int(raw)
    return key if MIN_KEY <= key <= MAX_KEY else None


# ------------------------------------------------------------------ ciphers

def build_permuted_alphabet(keyword):
    """Keyword letters first (first occurrence only), then the rest in order."""
    permuted = []
    for letter in keyword + "".join(ALPHABET):
        if letter not in permuted:
            permuted.append(letter)
    return permuted


def shift_text(text, key, alphabet):
    """Replace every letter by the one `key` positions further in `alphabet`.

    A negative key shifts backwards (used for decryption). Python's % always
    returns a value in 0..n-1, so (y - k) mod n never becomes negative.
    """
    position = {letter: i for i, letter in enumerate(alphabet)}
    return "".join(alphabet[(position[ch] + key) % N] for ch in text)


def caesar_encrypt(text, k):
    return shift_text(text, k, ALPHABET)          # c = (x + k) mod n


def caesar_decrypt(text, k):
    return shift_text(text, -k, ALPHABET)         # m = (y - k) mod n


def caesar2_encrypt(text, k1, keyword):
    return shift_text(text, k1, build_permuted_alphabet(keyword))


def caesar2_decrypt(text, k1, keyword):
    return shift_text(text, -k1, build_permuted_alphabet(keyword))


# ----------------------------------------------------------- user interface

def ask_choice(prompt, options):
    while True:
        choice = input(prompt).strip().upper()
        if choice in options:
            return choice
        print(f"  Error: please enter one of: {', '.join(options)}.")


def ask_key(prompt):
    while True:
        key = parse_key(input(prompt))
        if key is not None:
            return key
        print(f"  Error: the key must be an integer from {MIN_KEY} to {MAX_KEY} inclusive.")


def ask_text(prompt):
    while True:
        text, bad = normalize_text(input(prompt))
        if bad is not None:
            print(f"  Error: invalid character '{bad}'. Only letters of the Romanian "
                  "alphabet (A-Z, Ă, Â, Î, Ș, Ț, upper or lower case) and spaces are allowed.")
        elif not text:
            print("  Error: the text must contain at least one letter.")
        else:
            return text


def ask_keyword(prompt):
    while True:
        keyword, bad = normalize_text(input(prompt))
        if bad is not None:
            print(f"  Error: invalid character '{bad}' in the keyword. Only letters of the "
                  "Romanian alphabet (A-Z, Ă, Â, Î, Ș, Ț) are allowed.")
        elif len(keyword) < MIN_KEYWORD_LEN:
            print(f"  Error: the keyword must contain at least {MIN_KEYWORD_LEN} letters "
                  f"(you entered {len(keyword)}).")
        else:
            return keyword


def print_alphabet_table(title, alphabet):
    print(f"  {title}:")
    print("  " + " ".join(f"{i:>2}" for i in range(N)))
    print("  " + " ".join(f"{ch:>2}" for ch in alphabet))


def run_task_1_1():
    print("\n=== Task 1.1: Caesar cipher (Romanian alphabet, n = 31) ===")
    op = ask_choice("Operation - [E]ncrypt or [D]ecrypt: ", ["E", "D"])
    k = ask_key(f"Key k ({MIN_KEY}-{MAX_KEY}): ")
    if op == "E":
        m = ask_text("Message: ")
        print(f"  Prepared message: {m}")
        print(f"  Ciphertext:       {caesar_encrypt(m, k)}")
    else:
        c = ask_text("Ciphertext: ")
        print(f"  Decrypted message: {caesar_decrypt(c, k)}")


def run_task_1_2():
    print("\n=== Task 1.2: Caesar cipher with two keys (Romanian alphabet, n = 31) ===")
    op = ask_choice("Operation - [E]ncrypt or [D]ecrypt: ", ["E", "D"])
    k1 = ask_key(f"Key 1 - shift k1 ({MIN_KEY}-{MAX_KEY}): ")
    k2 = ask_keyword(f"Key 2 - keyword (at least {MIN_KEYWORD_LEN} Romanian letters): ")
    print(f"  Keyword: {k2}")
    print_alphabet_table("Original alphabet", ALPHABET)
    print_alphabet_table("Permuted alphabet", build_permuted_alphabet(k2))
    if op == "E":
        m = ask_text("Message: ")
        print(f"  Prepared message: {m}")
        print(f"  Ciphertext:       {caesar2_encrypt(m, k1, k2)}")
    else:
        c = ask_text("Ciphertext: ")
        print(f"  Decrypted message: {caesar2_decrypt(c, k1, k2)}")


def main():
    # Make sure Romanian letters are read and printed correctly on Windows.
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    while True:
        print("\n========== Laboratory Work No. 1 - Caesar Cipher ==========")
        print("1 - Task 1.1: Caesar cipher")
        print("2 - Task 1.2: Caesar cipher with a permutation (two keys)")
        print("0 - Exit")
        choice = ask_choice("Choose an option: ", ["1", "2", "0"])
        if choice == "1":
            run_task_1_1()
        elif choice == "2":
            run_task_1_2()
        else:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
