import socket
import time


def scan_tcp(target, port, timeout, retries=1):
    """Attempt TCP connect. If `timeout == 0`, perform a blocking connect
    (wait until connect succeeds or is refused) to avoid non-blocking
    EINPROGRESS (errno 115). Retries will re-run connect attempts.
    """
    last_state = "unknown"

    for attempt in range(max(1, int(retries))):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if timeout == 0:
                # blocking connect: wait until connection completes/refused
                sock.setblocking(True)
            else:
                sock.settimeout(timeout)

            sock.connect((target, port))
            return "open"

        except socket.timeout:
            last_state = "filtered"
        except ConnectionRefusedError:
            last_state = "closed"
        except BlockingIOError:
            # non-blocking operation in progress (EINPROGRESS) — treat as filtered
            last_state = "filtered"
        except OSError:
            last_state = "unknown"
        finally:
            try:
                sock.close()
            except Exception:
                pass

        # small backoff between retries
        if attempt < retries - 1:
            time.sleep(0.01)

    return last_state
