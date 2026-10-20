#!/data/data/com.termux/files/usr/bin/bash
set -eu

echo "[InstaGuard] Setting up a local-only Python lab..."
if ! command -v pkg >/dev/null 2>&1; then
  echo "[!] This installer is intended for Termux."
  echo "    Install Python 3 manually, then run: python instaguard.py --help"
  exit 1
fi

pkg update
pkg install -y python

chmod +x instaguard.py
echo
echo "[OK] Setup complete."
echo "Run: python instaguard.py --help"
echo "Example: python instaguard.py --wordlist ~/storage/downloads/wordlist.txt"
