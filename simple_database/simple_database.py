import json
import os
import time
from typing import Any, Dict, List, Tuple, Union

from .index import create_index, search_index
from .replication import Master, Slave


class SimpleDatabase:
    def __init__(
        self,
        data_path: str = "data.json",
        replication_master_ip: Union[str, None] = None,
        replication_master_port: int = 5000,
    ):
        self.data_path = data_path
        self.data: Dict[str, Any] = {}
        self.replication_master: Union[Master, None] = None
        self.replication_slave: Union[Slave, None] = None

        self.load_data()

        if replication_master_ip:
            self.replication_slave = Slave(
                self, replication_master_ip, replication_master_port
            )
        else:
            self.replication_master = Master(self, "0.0.0.0", replication_master_port)

    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

    def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def set(self, key: str, value: Any):
        if key not in self.data:
            self.data[key] = {"_created": time.time()}

        self.data[key]["_updated"] = time.time()
        self.data[key]["_rev"] = self.data.get(key, {}).get("_rev", 0) + 1
        self.data[key].update(value)

        if self.replication_master:
            self.replication_master.set_data(key, value)
        elif self.replication_slave:
            self.replication_slave.update_data(key, value)

    def delete(self, key: str):
        if key in self.data:
            del self.data[key]

        if self.replication_master:
            for slave in self.replication_master.slaves:
                slave.delete_data(key)

    def list_keys(self) -> List[str]:
        return list(self.data.keys())

    def list_values(self) -> List[Any]:
        return list(self.data.values())

    def create_index(self, column: str):
        create_index(self.data, column)

    def search_index(self, column: str, value: Any) -> List[str]:
        return search_index(self.data, column, value)

    def serialize(self, data: Any) -> str:
        return json.dumps(data)

    def deserialize(self, data: str) -> Any:
        return json.loads(data)
