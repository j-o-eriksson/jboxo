import socket
import subprocess


IP_ADDRESS = "127.0.0.1"
PORT = 4444


def start_vlc_server():
    """TODO: start service in separate thread."""
    subprocess.run(["cvlc", "--control=rc" f"--rc-host={IP_ADDRESS}:{PORT}"])


class VLCSession:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((IP_ADDRESS, PORT))
        print(str(self._receive()))

    def send_command(self, cmd: str) -> str:
        msg = bytes(cmd + "\r\n", "utf-8")
        self.s.sendall(msg)
        return self._receive()

    def _receive(self) -> str:
        data = []
        while True:
            chunk = self.s.recv(2048)
            data.append(chunk)
            print(f"received {len(chunk)} bytes")

            if b">" in chunk:
                break

        return (b''.join(data)).decode("utf-8")

