"""
salting_demo.py
----------------
Demonstrates why salting matters:
1. Without a salt, identical passwords produce identical hashes — trivially
   exploitable with a precomputed rainbow table, and it leaks "these two
   users have the same password" even without cracking anything.
2. With a per-user random salt, identical passwords produce DIFFERENT
   hashes, and an attacker must crack each one individually instead of
   reusing a single precomputed table across every account in a breach.

Usage:
    python3 salting_demo.py
"""

import hashlib
import secrets


def hash_unsalted(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def hash_salted(password: str, salt: bytes) -> str:
    return hashlib.sha256(salt + password.encode()).hexdigest()


def generate_salt(length: int = 16) -> bytes:
    """Cryptographically secure random salt. Never reuse this across users."""
    return secrets.token_bytes(length)


def store_format(salt: bytes, hashed: str) -> str:
    """Common storage convention: salt and hash concatenated with a separator,
    so the salt travels alongside the hash (it does NOT need to be secret)."""
    return f"{salt.hex()}${hashed}"


def verify(password: str, stored: str) -> bool:
    salt_hex, hashed = stored.split("$", 1)
    salt = bytes.fromhex(salt_hex)
    return hash_salted(password, salt) == hashed


def main():
    password = "password123"

    print("=" * 70)
    print("WITHOUT SALT: two users with the same password")
    print("=" * 70)
    user_a_hash = hash_unsalted(password)
    user_b_hash = hash_unsalted(password)
    print(f"User A hash: {user_a_hash}")
    print(f"User B hash: {user_b_hash}")
    print(f"Hashes identical? {user_a_hash == user_b_hash}")
    print("-> A single cracked/precomputed hash instantly reveals every user")
    print("   in the database who reused that same password.\n")

    print("=" * 70)
    print("WITH SALT: same password, unique random salt per user")
    print("=" * 70)
    salt_a = generate_salt()
    salt_b = generate_salt()
    hash_a = hash_salted(password, salt_a)
    hash_b = hash_salted(password, salt_b)

    print(f"User A salt: {salt_a.hex()}")
    print(f"User A hash: {hash_a}")
    print(f"User B salt: {salt_b.hex()}")
    print(f"User B hash: {hash_b}")
    print(f"Hashes identical? {hash_a == hash_b}")
    print("-> Even though both users picked 'password123', the stored hashes")
    print("   are completely different. An attacker can no longer use one")
    print("   precomputed rainbow table against the whole database — each")
    print("   hash must be attacked individually with its own salt.\n")

    print("=" * 70)
    print("STORAGE & VERIFICATION")
    print("=" * 70)
    stored_record = store_format(salt_a, hash_a)
    print(f"What you'd store in the DB for User A: {stored_record}")
    print(f"Login attempt with correct password: {verify(password, stored_record)}")
    print(f"Login attempt with wrong password:   {verify('wrongpass', stored_record)}")

    print("\nIMPORTANT CAVEAT: salting defeats *rainbow tables / batch cracking*")
    print("across many hashes. It does NOT make a single targeted hash immune")
    print("to brute-force or dictionary attack once the salt is known (and the")
    print("salt is normally stored right next to the hash, unencrypted, by")
    print("design — it doesn't need to be secret, it just needs to be unique).")
    print("That's why iteration count / algorithm choice (bcrypt, PBKDF2,")
    print("Argon2) still matters even with salting in place.")


if __name__ == "__main__":
    main()
