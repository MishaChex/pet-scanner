
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ScanConfig:
    target: str
    ports: List[int]
    timeout: float
    retries: int
    adaptive: bool
    verbose: bool
    scan_type: str
    max_workers: int = 10     # inactive
    json_output: Optional[str] = None
