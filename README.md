# Password Cracking and Hashing Algorithms

A cybersecurity internship project exploring how passwords are stored, why naive hashing is
breakable, and how brute-force / dictionary attacks actually work in practice — implemented
from scratch in Python, plus hands-on usage of industry-standard tools (Hashcat, John the Ripper).

## ⚠️ Ethical Use Notice

Everything in this repository operates **only on hashes you generate yourself** for learning
purposes. Do not run any of these tools or techniques against accounts, systems, or hash dumps
you do not own or do not have explicit written authorization to test. Unauthorized password
cracking is illegal in most jurisdictions (e.g. under the U.S. CFAA, UK Computer Misuse Act, etc.).
This project is for education and authorized security testing only.

## Objective

Analyze and implement brute-force password cracking techniques while understanding hash
functions and salting, in order to internalize why certain hashing choices make systems
secure or insecure.

## Tools Used

- **Python 3** — custom hashing, salting, brute-force, and dictionary-attack scripts
- **Hashcat** — GPU-accelerated password recovery tool
- **John the Ripper** — CPU-based password cracking tool

## Skills Learned

- How cryptographic hash functions (MD5, SHA-1, SHA-256, SHA-512) work and why fast hashes are
  unsuitable for password storage
- How salting defeats precomputed/rainbow-table attacks and prevents identical passwords from
  producing identical hashes
- How brute-force attacks scale exponentially with password length and character set size
- How dictionary attacks exploit human password reuse and predictable patterns
- Practical use of Hashcat and John the Ripper hash modes, attack modes, and rules
- Why slow, purpose-built password hashes (bcrypt, scrypt, Argon2, PBKDF2) resist cracking far
  better than general-purpose hashes

## Project Structure

```
password-cracking-hashing-project/
├── README.md
├── requirements.txt
├── src/
│   ├── hash_demo.py            # Hash functions + speed comparison (why MD5/SHA1 are weak for passwords)
│   ├── salting_demo.py         # Salting implementation + why it matters
│   ├── brute_force_cracker.py  # Custom brute-force cracker (character-set based)
│   └── dictionary_attack.py    # Custom dictionary/wordlist attack with mutation rules
├── wordlists/
│   └── sample_wordlist.txt     # Small sample wordlist for testing
├── hashcat_john_cheatsheet.md  # Real-world Hashcat & John the Ripper commands
└── report/
    └── FINDINGS_TEMPLATE.md    # Template to fill in with your own results/screenshots
```

## Setup

```bash
git clone <your-repo-url>
cd password-cracking-hashing-project
pip install -r requirements.txt
```

`requirements.txt` only lists `bcrypt`, which is optional — every script falls back to Python's
built-in `hashlib` (PBKDF2) if bcrypt isn't installed, so the demos work with zero dependencies too.

## Usage

### 1. Hash function demo — why MD5/SHA-1 are bad for passwords

```bash
python3 src/hash_demo.py
```

Hashes the same password with MD5, SHA-1, SHA-256, SHA-512, PBKDF2-SHA256, and bcrypt (if
available), shows that identical input → identical output (the core weakness), and benchmarks
how many hashes/second each algorithm can compute — illustrating why "fast" hashes let an
attacker try billions of guesses per second on a GPU, while bcrypt is deliberately slow.

### 2. Salting demo

```bash
python3 src/salting_demo.py
```

Shows two users with the same password producing the *same* hash when unsalted, and different
hashes once a random salt is added — defeating precomputed rainbow tables.

### 3. Custom brute-force cracker

```bash
# Demo mode: generates a random short password, hashes it, then cracks its own hash
python3 src/brute_force_cracker.py --demo --max-length 4

# Crack a specific hash you provide
python3 src/brute_force_cracker.py --hash 5f4dcc3b5aa765d61d8327deb882cf99 \
    --algo md5 --charset abcdefghijklmnopqrstuvwxyz0123456789 --max-length 5
```

### 4. Custom dictionary attack

```bash
# Demo mode
python3 src/dictionary_attack.py --demo --wordlist wordlists/sample_wordlist.txt

# Against a specific hash, with simple mutation rules (capitalization, appended digits/symbols)
python3 src/dictionary_attack.py --hash <hash> --algo sha256 \
    --wordlist wordlists/sample_wordlist.txt --mutations
```

### 5. Hashcat / John the Ripper

See [`hashcat_john_cheatsheet.md`](hashcat_john_cheatsheet.md) for ready-to-run commands against
a sample hash file, covering dictionary mode, brute-force/mask mode, and rule-based attacks.

## Key Takeaways (fill in after running your own tests)

| Algorithm | Hashes/sec (approx.) | Suitable for password storage? |
|---|---|---|
| MD5 | very high | No — too fast, broken collision resistance |
| SHA-1 | very high | No — too fast, deprecated for security use |
| SHA-256/512 | high | No (alone) — still too fast without salting+iteration |
| PBKDF2 (100k iter) | low | Yes, when configured with enough iterations |
| bcrypt | very low (by design) | Yes — industry standard for password storage |

Run `hash_demo.py` to generate your own numbers for this table on your machine and paste them
into your final report.

## License

MIT — for educational use.
