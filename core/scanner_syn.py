from scapy.all import IP, TCP, sr1, send
import random
import time


def scan_syn(target, port, timeout, retries=1):
    """Perform a SYN scan using scapy. If `timeout == 0` use blocking wait
    (pass `timeout=None` to `sr1`) to avoid immediate timeout.
    Retries are supported with a small backoff.
    """
    last_state = "filtered"

    for attempt in range(max(1, int(retries))):
        src_port = random.randint(1024, 65535)

        packet = IP(dst=target) / TCP(
            sport=src_port,
            dport=port,
            flags="S"
        )

        # scapy: timeout=None will wait indefinitely
        call_timeout = None if timeout == 0 else timeout

        try:
            response = sr1(packet, timeout=call_timeout, verbose=0)
        except Exception:
            response = None

        if response is None:
            last_state = "filtered"
        else:
            if response.haslayer(TCP):
                tcp_layer = response.getlayer(TCP)

                if tcp_layer.flags == 0x12:
                    rst = IP(dst=target) / TCP(
                        sport=src_port,
                        dport=port,
                        flags="R"
                    )
                    send(rst, verbose=0)
                    return "open"

                elif tcp_layer.flags == 0x14:
                    return "closed"

            last_state = "unknown"

        if attempt < retries - 1:
            time.sleep(0.01)

    return last_state
