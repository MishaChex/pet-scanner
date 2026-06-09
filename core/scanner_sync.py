from core.services import COMMON_PORTS
from core.scanner_tcp import scan_tcp as scan_tcp_port
from core.scanner_udp import scan_udp as scan_udp_port
from core.scanner_syn import scan_syn as scan_tcp_syn_port
from utils.ports import parse_ports

import argparse