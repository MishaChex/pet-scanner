import argparse
from core.engine import ScanEngine
from config import ScanConfig
from core.services import COMMON_PORTS
from utils.ports import parse_ports
import time


def build_parser():
    parser = argparse.ArgumentParser(
        prog="lvns",
        description="Lightweight Vulnerability & Network scan"
    )

    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Run port scan")

    scan_parser.add_argument("target", help="Target IP address")
    scan_parser.add_argument(
        "-p", "--ports",
        default="1-1024",
        help="Port range (e.g. 80,443 or 1-1000) or common"
    )
    scan_parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=0.1,
        help="Connection timeout in seconds"
    )
    scan_parser.add_argument(
        "-r", "--retries",
        type=int,
        default=1,
        help="Number of retries per port"
    )
    scan_parser.add_argument(
        "-a", "--adaptive",
        action="store_true",
        help="Enable adaptive timeout"
    )
    scan_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    scan_parser.add_argument(
        "-j", "--json",
        help="Export results to JSON file"
    )
    scan_parser.add_argument(
        "-w", "--workers",
        type=int,
        default=10,
        help="Number of concurrent workers"
    )
    scan_parser.add_argument(
        "-s", "--scan-type",
        choices=["tcp", "syn", "udp"],
        default="tcp",
        help="Scan type: tcp (connect), syn (stealth), udp"
    )
    
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        try:
            ports = parse_ports(args.ports)
        except ValueError as e:
            parser.error(str(e))

        config = ScanConfig(
            target=args.target,
            ports=ports,
            timeout=args.timeout,
            retries=args.retries,
            adaptive=args.adaptive,
            verbose=args.verbose,
            scan_type=args.scan_type,
            max_workers=args.workers,
            json_output=args.json
        )

        engine = ScanEngine(config)
        start_time = time.monotonic()
        results = engine.run()

        print(f"Scanning {config.target}")
        print(f"{'PORT':<6} {'STATE':<12} SERVICE")
        print("-" * 40)

        for port, state in zip(config.ports, results):
            service = COMMON_PORTS.get(port, "unknown")

            if config.scan_type == "syn":
                if state != "closed":
                    print(f"{port:<6} {state:<12} {service}")
            else:
                if config.verbose:
                    print(f"{port:<6} {state:<12} {service}")
                else:
                    if isinstance(state, str) and state.startswith("open"):
                        print(f"{port:<6} {state:<12} {service}")

        if config.json_output:
            import json
            out = []
            for port, state in zip(config.ports, results):
                out.append({"port": port, "state": state, "service": COMMON_PORTS.get(port, "unknown")})
            with open(config.json_output, "w") as f:
                json.dump(out, f, indent=2)

        # Print elapsed time
        elapsed = time.monotonic() - start_time
        print("-" * 40)
        print(f"Scan completed in {elapsed:.3f} seconds")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
