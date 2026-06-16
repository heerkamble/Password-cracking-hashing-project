# Internship Project Findings — Password Cracking and Hashing Algorithms

**Name:**
**Date:**
**Supervisor / Team:**

## 1. Objective Recap

Briefly restate the objective in your own words.

## 2. Hash Function Comparison

Paste your `hash_demo.py` output here. Fill in the table:

| Algorithm | Hashes/sec (your machine) | Suitable for password storage? | Why / why not |
|---|---|---|---|
| MD5 | | | |
| SHA-1 | | | |
| SHA-256 | | | |
| SHA-512 | | | |
| PBKDF2 | | | |
| bcrypt | | | |

## 3. Salting

- What happened when you hashed the same password twice without a salt?
- What happened once you added a salt?
- Why doesn't salting alone protect against an attack on a *single* known hash?

## 4. Custom Brute-Force Cracker Results

| Password length | Charset size | Search space | Time to crack |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

Observation: how does time-to-crack scale as length increases by 1 character? (It should
roughly multiply by the charset size — explain why in your own words.)

## 5. Custom Dictionary Attack Results

- Did the base wordlist crack your test password? (Y/N)
- Did enabling `--mutations` change the result? What mutation found it (capitalization /
  appended digits / leetspeak)?
- What does this tell you about real-world password choices like `Password123!`?

## 6. Hashcat / John the Ripper Results

| Tool | Attack mode | Hash | Time to crack |
|---|---|---|---|
| Hashcat | dictionary | | |
| Hashcat | mask/brute-force | | |
| John | dictionary + rules | | |

Screenshot placeholders:
- [ ] Hashcat dictionary attack output
- [ ] Hashcat mask attack output
- [ ] John the Ripper `--show` output

## 7. Key Takeaways

Summarize, in 4–6 sentences, what this project taught you about:
1. Why password hashing algorithm choice matters
2. Why salting matters (and its limits)
3. What makes a password actually resistant to cracking
4. One recommendation you'd make to a development team storing user passwords

## 8. References

- Hashcat documentation: https://hashcat.net/wiki/
- John the Ripper documentation: https://www.openwall.com/john/doc/
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
