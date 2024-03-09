import os
import socket
import subprocess

import psutil
from dotenv import load_dotenv

load_dotenv()

STORAGE_PATH = os.getenv("BIN_PATH")
STORAGE_NAME = os.getenv("STORAGE_NAME")
SOCKET_PATH = os.getenv("SOCKET_PATH")


class TokenStorage:
    def __init__(
        self,
        bin_path=STORAGE_PATH,
        socket_path=SOCKET_PATH,
    ):
        self.socket_path = socket_path
        process = self.get_process()
        if process is None:
            print("Starting storage process")
            bin_path = os.path.expanduser(bin_path)
            self.process = subprocess.Popen([bin_path])

    @staticmethod
    def get_process():
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] == STORAGE_NAME:
                return proc
        return None

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self.socket_path)
        return sock

    def send_token(self, token):
        sock = self.connect()
        sock.sendall(token.encode("utf-8"))
        response = sock.recv(1024)
        print(response.decode("utf-8"))
        sock.close()

    def request_token(self):
        sock = self.connect()
        sock.sendall("get_token".encode("utf-8"))
        response = sock.recv(1024)
        token = response.decode("utf-8")
        sock.close()
        return token

    def terminate(self):
        proc = self.get_process()
        if proc is not None:
            proc.terminate()
