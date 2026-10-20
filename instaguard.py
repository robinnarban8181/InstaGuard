#!/usr/bin/env python3
"""InstaGuard: local-only authentication security training lab.

This program never opens network connections. It simulates an Instagram-style
login locally to demonstrate wordlists, failed-attempt counters, rate limiting,
and account lockout.
"""
from __future__ import annotations

import argparse
import getpass
import time
from pathlib import Path


def load_wordlist(path: Path):
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                candidate = line.rstrip("\r\n")
                if candidate:
                    yield candidate
    except OSError as exc:
        raise SystemExit(f"[!] Could not read wordlist: {exc}")


def run_lab(args):
    print("=" * 58)
    print("InstaGuard | LOCAL-ONLY LOGIN SECURITY LAB")
    print("No network requests are made by this program.")
    print("=" * 58)

    username = args.username
    correct_password = args.demo_password
    max_attempts = max(1, args.max_attempts)
    delay = max(0.0, args.delay)
    lockout_seconds = max(0, args.lockout_seconds)

    print(f"Demo account: {username}")
    print(f"Lockout threshold: {max_attempts} consecutive failed attempts")
    print(f"Simulated delay per attempt: {delay:.2f}s")
    print("This is a toy simulation, not a real Instagram integration.\n")

    if args.wordlist:
        candidates = load_wordlist(Path(args.wordlist))
        print(f"Wordlist mode: {args.wordlist}")
        print("Candidates will be checked only against the local demo password.")
    else:
        print("Interactive mode: enter a password to simulate one login attempt.")
        candidates = None

    failed = 0
    total = 0
    locked_until = 0.0

    def check(candidate: str) -> bool:
        nonlocal failed, total, locked_until
        now = time.monotonic()
        if now < locked_until:
            remaining = int(locked_until - now + 0.999)
            print(f"[LOCKED] Login blocked for {remaining}s.")
            return False

        total += 1
        if delay:
            time.sleep(delay)

        if candidate == correct_password:
            print(f"[SUCCESS] Local demo password matched after {total} attempt(s).")
            failed = 0
            return True

        failed += 1
        print(f"[FAIL] Attempt {total}: incorrect ({failed}/{max_attempts} failures)")
        if failed >= max_attempts:
            print("[DEFENSE] Account lockout threshold reached.")
            if lockout_seconds:
                locked_until = time.monotonic() + lockout_seconds
                print(f"[DEFENSE] Simulated lockout for {lockout_seconds}s.")
            else:
                print("[DEFENSE] Further attempts stopped for this run.")
                raise StopIteration
        return False

    try:
        if candidates is not None:
            for candidate in candidates:
                if check(candidate):
                    break
                if locked_until and time.monotonic() < locked_until:
                    # Do not wait out a lockout in wordlist mode.
                    print("[STOP] Wordlist run stopped because the account is locked.")
                    break
                if failed >= max_attempts:
                    break
            else:
                print("[DONE] End of wordlist reached.")
        else:
            for _ in range(max_attempts + 1):
                candidate = getpass.getpass("Demo password: ")
                try:
                    if check(candidate):
                        break
                except StopIteration:
                    break
    except StopIteration:
        pass

    print("\n--- Lab summary ---")
    print(f"Total login attempts: {total}")
    print(f"Failed attempts: {failed}")
    print(f"Lockout threshold: {max_attempts}")
    print("Network activity: none")


def main():
    parser = argparse.ArgumentParser(
        description="Local-only login security lab; no network requests."
    )
    parser.add_argument("--wordlist", help="Path to a local wordlist text file")
    parser.add_argument("--username", default="demo_user", help="Simulated username")
    parser.add_argument(
        "--demo-password",
        default="LabPass123!",
        help="Password for the local simulated account (default: LabPass123!)",
    )
    parser.add_argument(
        "--max-attempts", type=int, default=5,
        help="Stop after this many consecutive failures (default: 5)",
    )
    parser.add_argument(
        "--delay", type=float, default=0.5,
        help="Simulated delay per attempt in seconds (default: 0.5)",
    )
    parser.add_argument(
        "--lockout-seconds", type=int, default=10,
        help="Demonstrate a lockout for this many seconds (default: 10)",
    )
    args = parser.parse_args()
    run_lab(args)


if __name__ == "__main__":
    main()
