from core.scanner_tcp import scan_tcp
from core.scanner_udp import scan_udp
from core.scanner_syn import scan_syn


class ScanEngine:

    def __init__(self, config):
        self.config = config

    def run(self):

        if self.config.scan_type == "tcp":
            scanner = scan_tcp

        elif self.config.scan_type == "udp":
            scanner = scan_udp

        elif self.config.scan_type == "syn":
            scanner = scan_syn

        else:
            raise ValueError("Unknown scan type")

        results = []

        for port in self.config.ports:
            result = scanner(
                target=self.config.target,
                port=port,
                timeout=self.config.timeout,
                retries=self.config.retries
            )
            results.append(result)

        return results
