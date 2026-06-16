# Hashcat & John the Ripper Cheat Sheet

Practical commands for the industry-standard tools, to run alongside the custom Python scripts
in `src/`. Run these only against hashes you generated yourself for this project.

## 1. Setup: create a sample hash file

```bash
# Generate an MD5 hash of a test password to crack
echo -n "letmein123" | md5sum
# Save the resulting hash into a file, one hash per line
echo "0d10c1e6e7e0a1b3a2c4f5e6d7c8b9a0" > hashes.txt
```

(In practice, replace this with real hashes exported from a test system you're authorized to
audit — e.g. `/etc/shadow` entries from a VM you control, or hashes you generated with the
Python scripts in this repo.)

## Hashcat

Hashcat identifies hash types by **mode number** (`-m`). Common ones:

| Mode | Hash type |
|---|---|
| 0 | MD5 |
| 100 | SHA1 |
| 1400 | SHA256 |
| 1700 | SHA512 |
| 1000 | NTLM |
| 3200 | bcrypt |

### Dictionary attack
```bash
hashcat -m 0 -a 0 hashes.txt wordlists/sample_wordlist.txt
```
- `-a 0` = straight/dictionary attack mode

### Dictionary + rules (mutations: capitalization, leetspeak, appended digits)
```bash
hashcat -m 0 -a 0 hashes.txt wordlists/sample_wordlist.txt -r rules/best64.rule
```

### Brute-force / mask attack
```bash
# ?l = lowercase letter, ?d = digit, ?u = uppercase, ?s = symbol
hashcat -m 0 -a 3 hashes.txt ?l?l?l?l?d?d
```
- `-a 3` = brute-force/mask mode
- The mask above tries: 4 lowercase letters + 2 digits

### Combinator attack (combine two wordlists)
```bash
hashcat -m 0 -a 1 hashes.txt wordlists/sample_wordlist.txt wordlists/sample_wordlist.txt
```

### View cracked results
```bash
hashcat -m 0 hashes.txt --show
```

## John the Ripper

### Basic dictionary attack
```bash
john --wordlist=wordlists/sample_wordlist.txt hashes.txt
```

### With mutation rules
```bash
john --wordlist=wordlists/sample_wordlist.txt --rules hashes.txt
```

### Pure brute-force (incremental mode)
```bash
john --incremental hashes.txt
```

### Specify hash format explicitly
```bash
john --format=raw-md5 --wordlist=wordlists/sample_wordlist.txt hashes.txt
```

### Show cracked passwords
```bash
john --show hashes.txt
```

### Cracking /etc/shadow-style files (on a VM you control)
```bash
unshadow /etc/passwd /etc/shadow > combined.txt
john combined.txt
```

## Comparing your custom scripts vs. Hashcat/John

| Aspect | Python scripts (this repo) | Hashcat / John |
|---|---|---|
| Purpose | Make the algorithm visible/understandable | Production-grade cracking at scale |
| Speed | Thousands–millions/sec (CPU, single-threaded) | Billions/sec (GPU) for fast hashes |
| Rules engine | A few hand-coded mutations | Extensive rule files, masks, hybrid modes |
| Best for | Learning *why* an attack works | Actually auditing password strength at scale |

For your report: run the same target hash through both your Python script and Hashcat/John,
and compare time-to-crack. The gap illustrates exactly why real-world password policies need to
account for GPU-accelerated attackers, not just "a person guessing by hand."
