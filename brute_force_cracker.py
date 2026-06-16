"""
brute_force_cracker.py
-----------------------
A from-scratch brute-force password cracker. Generates every possible
combination of characters up to a max length and checks each one against a
target hash, until it finds a match.

This is for cracking hashes YOU generated, to understand how attack
complexity scales with password length and character-set size. It is not
optimized like Hashcat/John (which use GPUs and precomputed tables) — it's
meant to make the underlying algorithm visible.

Usage:
    # Demo mode: script picks a random short password, hashes it, cracks it
    python3 brute_force_cracker.py --demo --max-length 4

    # Crack a specific hash
    python3 brute_force_cracker.py --hash <hex digest> --algo sha256 \
        --charset abcdefghijklmnopqrstuvwxyz --max-length 5
"""

import argparse
import hashlib
import itertools
import random
import string
import time

ALGOS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def compute_hash(text: str, algo: str) -> str:
    return ALGOS[algo](text.encode()).hexdigest()


def brute_force(target_hash: str, algo: str, charset: str, max_length: int):
    """Yields progress and returns the cracked password, or None."""
    attempts = 0
    start = time.perf_counter()

    for length in range(1, max_length + 1):
        total_for_length = len(charset) ** length
        print(f"[*] Trying length {length} ({total_for_length:,} combinations)...")
        for combo in itertools.product(charset, repeat=length):
            candidate = "".join(combo)
            attempts += 1
            if compute_hash(candidate, algo) == target_hash:
                elapsed = time.perf_counter() - start
                return candidate, attempts, elapsed

    elapsed = time.perf_counter() - start
    return None, attempts, elapsed


def main():
    parser = argparse.ArgumentParser(description="Educational brute-force password cracker.")
    parser.add_argument("--hash", help="Target hash (hex digest) to crack")
    parser.add_argument("--algo", choices=ALGOS.keys(), default="md5", help="Hash algorithm")
    parser.add_argument(
        "--charset",
        default=string.ascii_lowercase + string.digits,
        help="Characters to try (default: a-z0-9)",
    )
    parser.add_argument("--max-length", type=int, default=4, help="Maximum password length to try")
    parser.add_argument("--demo", action="store_true", help="Generate a random password and crack it")
    args = parser.parse_args()

    if args.demo:
        secret_password = "".join(random.choices(args.charset, k=min(4, args.max_length)))
        target_hash = compute_hash(secret_password, args.algo)
        print(f"[DEMO] Secretly generated password: {secret_password!r}")
        print(f"[DEMO] Its {args.algo.upper()} hash:            {target_hash}")
        print("[DEMO] Now attempting to crack it WITHOUT looking at the plaintext above...\n")
    else:
        if not args.hash:
            parser.error("--hash is required unless --demo is used")
        target_hash = args.hash.lower()

    estimated_total = sum(len(args.charset) ** n for n in range(1, args.max_length + 1))
    print(f"[*] Charset: {args.charset!r} ({len(args.charset)} characters)")
    print(f"[*] Max length: {args.max_length}")
    print(f"[*] Worst-case search space: {estimated_total:,} combinations\n")

    result, attempts, elapsed = brute_force(target_hash, args.algo, args.charset, args.max_length)

    print()
    if result is not None:
        print(f"[+] CRACKED: {result!r}")
    else:
        print("[-] Not found within the given length/charset constraints.")
    print(f"[*] Attempts: {attempts:,}")
    print(f"[*] Time elapsed: {elapsed:.2f}s")
    if elapsed > 0:
        print(f"[*] Rate: {attempts / elapsed:,.0f} attempts/sec")


if __name__ == "__main__":
    main()
