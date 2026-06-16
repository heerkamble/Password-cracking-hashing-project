"""
dictionary_attack.py
---------------------
A from-scratch dictionary (wordlist) attack. Tries every word in a wordlist
against a target hash, optionally applying simple "mutation rules" that
mimic how real humans modify base words to (try to) make them more secure —
capitalizing the first letter, appending common digits, appending common
symbols, leetspeak substitutions. These mirror the kind of rule files
Hashcat (-r) and John (--rules) apply automatically at much larger scale.

Usage:
    python3 dictionary_attack.py --demo --wordlist wordlists/sample_wordlist.txt

    python3 dictionary_attack.py --hash <hex digest> --algo sha256 \
        --wordlist wordlists/sample_wordlist.txt --mutations
"""

import argparse
import hashlib
import time

ALGOS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}

LEET_MAP = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$"}
COMMON_SUFFIXES = ["", "1", "12", "123", "1234", "!", "01", "2023", "2024", "2025", "2026"]


def compute_hash(text: str, algo: str) -> str:
    return ALGOS[algo](text.encode()).hexdigest()


def leetspeak(word: str) -> str:
    return "".join(LEET_MAP.get(c, c) for c in word)


def generate_mutations(word: str):
    """Yields the base word plus common human-pattern variations."""
    bases = {word, word.lower(), word.capitalize(), word.upper(), leetspeak(word)}
    for base in bases:
        for suffix in COMMON_SUFFIXES:
            yield base + suffix


def load_wordlist(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if word:
                yield word


def dictionary_attack(target_hash: str, algo: str, wordlist_path: str, use_mutations: bool):
    attempts = 0
    start = time.perf_counter()

    for word in load_wordlist(wordlist_path):
        candidates = generate_mutations(word) if use_mutations else [word]
        for candidate in candidates:
            attempts += 1
            if compute_hash(candidate, algo) == target_hash:
                elapsed = time.perf_counter() - start
                return candidate, attempts, elapsed

    elapsed = time.perf_counter() - start
    return None, attempts, elapsed


def main():
    parser = argparse.ArgumentParser(description="Educational dictionary/wordlist password attack.")
    parser.add_argument("--hash", help="Target hash (hex digest) to crack")
    parser.add_argument("--algo", choices=ALGOS.keys(), default="sha256", help="Hash algorithm")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("--mutations", action="store_true", help="Apply common mutation rules")
    parser.add_argument("--demo", action="store_true", help="Pick a random word from the list and crack it")
    args = parser.parse_args()

    if args.demo:
        import random
        words = list(load_wordlist(args.wordlist))
        secret_password = random.choice(words) + random.choice(["", "1", "123", "!"])
        target_hash = compute_hash(secret_password, args.algo)
        print(f"[DEMO] Secretly chosen password: {secret_password!r}")
        print(f"[DEMO] Its {args.algo.upper()} hash:          {target_hash}")
        print("[DEMO] Now attempting to crack it via dictionary attack...\n")
        use_mutations = True
    else:
        if not args.hash:
            parser.error("--hash is required unless --demo is used")
        target_hash = args.hash.lower()
        use_mutations = args.mutations

    print(f"[*] Wordlist: {args.wordlist}")
    print(f"[*] Mutations enabled: {use_mutations}\n")

    result, attempts, elapsed = dictionary_attack(target_hash, args.algo, args.wordlist, use_mutations)

    print()
    if result is not None:
        print(f"[+] CRACKED: {result!r}")
    else:
        print("[-] Not found in this wordlist (try --mutations, or a larger wordlist).")
    print(f"[*] Attempts: {attempts:,}")
    print(f"[*] Time elapsed: {elapsed:.3f}s")


if __name__ == "__main__":
    main()
