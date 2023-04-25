import socket
import threading
import time
from typing import Any, Dict, Tuple


class Master:
    def __init__(self, db: "SimpleDatabase", ip_address: str, port: int):
        self.db = db
        self.ip_address = ip_address
        self.port = port
        self.server_socket = None
        self.slaves = []
        self.thread = threading.Thread(target=self.accept_slaves)
        self.thread.start()

    def accept_slaves(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, self.port))
        self.server_socket.listen(1)
        while True:
            conn, addr = self.server_socket.accept()
            slave = SlaveConnection(self.db, conn, addr)
            self.slaves.append(slave)

    def get_data(self, key: str) -> Any:
        return self.db.get(key)

    def set_data(self, key: str, value: Any):
        self.db.set(key, value)
        for slave in self.slaves:
            slave.update_data(key, value)


class Slave:
    def __init__(self, db: "SimpleDatabase", master_ip: str, master_port: int):
        self.db = db
        self.master_ip = master_ip
        self.master_port = master_port
        self.thread = threading.Thread(target=self.poll_master)
        self.thread.start()

    def poll_master(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.master_ip, self.master_port))
                    s.sendall(b"ping")
                    data = s.recv(1024)
                    if data == b"pong":
                        self.sync_data()
                    else:
                        time.sleep(1)
            except ConnectionRefusedError:
                time.sleep(1)

    def sync_data(self):
        for key in self.db.data.keys():
            if key not in ("_id", "_rev", "_created", "_updated"):
                value = self.get_data_from_master(key)
                self.db.set(key, value)

    def get_data_from_master(self, key: str) -> Any:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.master_ip, self.master_port))
            s.sendall(f"get {key}".encode())
            data = s.recv(1024)
           
            if data == b"not found":
                return None

            return self.db.deserialize(data)

    def update_data(self, key: str, value: Any):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.master_ip, self.master_port))
            s.sendall(f"set {key} {self.db.serialize(value)}".encode())

