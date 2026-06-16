"""
hash_demo.py
------------
Demonstrates several cryptographic hash functions applied to passwords, and
benchmarks how fast each one can be computed. The benchmark is the whole
point: a hash function that's "fast" is *bad* for password storage, because
it lets an attacker try billions of guesses per second. Purpose-built slow
hashes (PBKDF2 with many iterations, bcrypt, scrypt, Argon2) are designed to
resist exactly this.

Usage:
    python3 hash_demo.py
"""

import hashlib
import time

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False


def hash_md5(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def hash_sha1(password: str) -> str:
    return hashlib.sha1(password.encode()).hexdigest()


def hash_sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def hash_sha512(password: str) -> str:
    return hashlib.sha512(password.encode()).hexdigest()


def hash_pbkdf2(password: str, salt: bytes = b"static-demo-salt", iterations: int = 100_000) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations).hex()


def hash_bcrypt(password: str) -> str:
    if not BCRYPT_AVAILABLE:
        return "(bcrypt not installed — run `pip install bcrypt`)"
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()


def benchmark(func, password: str, iterations: int = 2000, **kwargs) -> float:
    """Returns hashes/second for the given hash function."""
    start = time.perf_counter()
    for _ in range(iterations):
        func(password, **kwargs) if kwargs else func(password)
    elapsed = time.perf_counter() - start
    return iterations / elapsed if elapsed > 0 else float("inf")


def main():
    password = "Summer2024!"

    print("=" * 70)
    print("PART 1: Same password -> what does each algorithm produce?")
    print("=" * 70)
    print(f"Plaintext password: {password!r}\n")
    print(f"MD5:            {hash_md5(password)}")
    print(f"SHA-1:          {hash_sha1(password)}")
    print(f"SHA-256:        {hash_sha256(password)}")
    print(f"SHA-512:        {hash_sha512(password)}")
    print(f"PBKDF2-SHA256:  {hash_pbkdf2(password)}")
    print(f"bcrypt:         {hash_bcrypt(password)}")

    print("\n" + "=" * 70)
    print("PART 2: Identical passwords ALWAYS produce identical unsalted hashes")
    print("=" * 70)
    print("This is exactly why attackers use precomputed rainbow tables —")
    print("if two users both pick 'password123', their unsalted hashes match.\n")
    print(f"User A ('password123') SHA-256: {hash_sha256('password123')}")
    print(f"User B ('password123') SHA-256: {hash_sha256('password123')}")
    print("-> Identical. See salting_demo.py for the fix.")

    print("\n" + "=" * 70)
    print("PART 3: Speed benchmark — why fast hashing is dangerous for passwords")
    print("=" * 70)
    print("Lower hashes/sec = harder for an attacker to brute-force at scale.\n")

    results = {
        "MD5": benchmark(hash_md5, password, iterations=20000),
        "SHA-1": benchmark(hash_sha1, password, iterations=20000),
        "SHA-256": benchmark(hash_sha256, password, iterations=20000),
        "SHA-512": benchmark(hash_sha512, password, iterations=20000),
        "PBKDF2 (100k iter)": benchmark(hash_pbkdf2, password, iterations=20),
    }
    if BCRYPT_AVAILABLE:
        results["bcrypt (12 rounds)"] = benchmark(hash_bcrypt, password, iterations=20)

    for name, rate in sorted(results.items(), key=lambda x: -x[1]):
        print(f"{name:<22}: {rate:>12,.1f} hashes/sec")

    print("\nNote: on a real attacker's GPU rig, MD5/SHA-1/SHA-256 rates would be")
    print("in the BILLIONS/sec, while bcrypt stays in the low thousands or less —")
    print("that gap is the entire reason password hashing algorithms exist.")

    if not BCRYPT_AVAILABLE:
        print("\n(Install bcrypt with `pip install bcrypt` to include it in this benchmark.)")


if __name__ == "__main__":
    main()
