from typing import List
from core.services import COMMON_PORTS


def parse_ports(value: str) -> List[int]:
    """Parse port input strings into a sorted list of ints.

    Supported formats:
    - "common" -> returns keys from COMMON_PORTS
    - "80,443,8080" -> comma separated ports
    - "1-1024" -> range (inclusive)
    - mixed like "22,80,1000-1005"
    """
    if value is None:
        return []

    value = value.strip()
    if value == "common":
        return sorted(int(p) for p in COMMON_PORTS.keys())

    ports = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                start_s, end_s = part.split("-", 1)
                start = int(start_s)
                end = int(end_s)
            except ValueError:
                raise ValueError(f"Invalid port range: {part}")
            if start > end:
                start, end = end, start
            ports.update(range(start, end + 1))
        else:
            try:
                ports.add(int(part))
            except ValueError:
                raise ValueError(f"Invalid port value: {part}")

    return sorted(p for p in ports if 0 < p <= 65535)
