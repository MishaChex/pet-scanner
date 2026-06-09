pet-scanner
===========

Lightweight port scanner (educational/demo project).

Overview
--------
This project provides simple TCP/UDP/SYN port scanning utilities and a small CLI.
It is organized into a `core/` package containing scanner implementations and small helpers, plus `utils/` helpers and a simple `cli.py` entrypoint.

Requirements
------------
- Python 3.8+
- Optional: `scapy` for SYN scans (install with `pip install scapy`).

Quick install
-------------
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install scapy
```

Usage
-----
Run the CLI entrypoint `cli.py`:

```bash
python3 cli.py scan <target> -p <ports> [options]
```

Examples
```
python3 cli.py scan 192.168.1.10 -p 22,80
python3 cli.py scan example.com -p common -s syn  # requires scapy and usually root
python3 cli.py scan 10.0.0.5 -p 1-1024 -v       # verbose: show all scanned ports
python3 cli.py scan 1.2.3.4 -p 22,80 -j out.json
```

Notes about timeouts
--------------------
- The scanners accept a `timeout` value in seconds. If you pass `0` as the timeout, the scanner will switch to a blocking wait for the specific step (connect/recv/sr1). This is intentional: it waits for the operation to complete instead of returning immediately with a non-blocking-in-progress error (EINPROGRESS / errno 115).
- Warning: `timeout==0` can block for a long time if the remote host doesn't respond. Use with care.
