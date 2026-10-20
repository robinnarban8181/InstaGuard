# InstaGuard — Termux Local Login Security Lab

InstaGuard is a **local-only educational simulation** for learning how password
wordlists, failed-login counters, rate limiting, and account lockout work.

**It does not connect to Instagram or any other website. It sends no network
requests and cannot log in to real accounts.**

## Features

- Python 3; no third-party Python packages required
- Reads an existing newline-separated wordlist
- Simulates an Instagram-style login prompt locally
- Counts failed attempts
- Demonstrates per-attempt delay (simulated rate limiting)
- Stops after a configurable failed-attempt threshold
- Prints a final summary

## Folder structure

```text
InstaGuard/
├── instaguard.py
├── install.sh
└── README.md
```

## Install on Termux

1. Open Termux.
2. Enter the project directory.
3. Run:

```bash
bash install.sh
```

If you already have Python 3 installed, you can skip the installer and run the
Python file directly.

## Run interactive mode

```bash
python instaguard.py
```

The default local demo password is `LabPass123!`. This is a deliberately
known training password, not a real account password.

## Run with your existing wordlist

First enable shared-storage access if your wordlist is in Downloads:

```bash
termux-setup-storage
```

Then run (replace the filename with your actual file):

```bash
python instaguard.py --wordlist ~/storage/downloads/wordlist.txt
```

By default, the simulated password is `LabPass123!`, so the wordlist will only
report a match if that exact string is present. You can set a different demo
password for the lab:

```bash
python instaguard.py --wordlist ~/storage/downloads/wordlist.txt --demo-password 'ExampleLabPass!'
```

## Demonstrate lockout and rate limiting

```bash
python instaguard.py --max-attempts 3 --delay 1 --lockout-seconds 15
```

- `--max-attempts 3`: stop after three consecutive failures
- `--delay 1`: wait one second per simulated attempt
- `--lockout-seconds 15`: display a simulated 15-second lockout

This is a teaching simulation, not a production authentication system. The
delay and lockout are implemented locally and do not test a real service.

## Options

```text
python instaguard.py --help
```

- `--wordlist PATH` — local text file with one candidate per line
- `--username NAME` — simulated username (default `demo_user`)
- `--demo-password VALUE` — local demo password (default `LabPass123!`)
- `--max-attempts N` — failed-attempt threshold (default `5`)
- `--delay SECONDS` — simulated delay per attempt (default `0.5`)
- `--lockout-seconds N` — simulated lockout duration (default `10`)

## Safety

Use only for local learning. This project intentionally has no HTTP, browser,
Instagram, credential submission, proxy, CAPTCHA, or remote-login functionality.
Do not use password lists against accounts or services without explicit
authorization.
