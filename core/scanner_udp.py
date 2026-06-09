import socket
import time


def scan_udp(target, port, timeout, retries=1):
    """Send an empty UDP datagram and wait for a response.

    If `timeout == 0`, perform a blocking recv to wait for a reply/ICMP.
    Retries are supported with a small backoff.
    """
    last_state = "open|filtered"

    for attempt in range(max(1, int(retries))):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            if timeout == 0:
                sock.setblocking(True)
            else:
                sock.settimeout(timeout)

            sock.sendto(b"", (target, port))
            sock.recvfrom(1024)
            return "open"
        except socket.timeout:
            last_state = "open|filtered"
        except ConnectionRefusedError:
            last_state = "closed"
        except OSError:
            last_state = "unknown"
        finally:
            try:
                sock.close()
            except Exception:
                pass

        if attempt < retries - 1:
            time.sleep(0.01)

    return last_state
