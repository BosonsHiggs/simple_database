import json
import os
import time
from typing import Any, Dict, List, Tuple, Union

import asyncio
import aiohttp


class AsyncSimpleDatabase:
    def __init__(
        self,
        data_path: str = "data.json",
        replication_master_ip: Union[str, None] = None,
        replication_master_port: int = 5000,
    ):
        self.data_path = data_path
        self.data: Dict[str, Any] = {}
        self.indexes: Dict[str, Dict] = {}
        self.replication_master: Union[str, None] = replication_master_ip
        self.replication_master_port = replication_master_port

        self.load_data()

    async def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

            self.create_indexes()

    async def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)

    async def get(self, key: str) -> Any:
        return self.data.get(key)

    async def set(self, key: str, value: Any):
        if key not in self.data:
            self.data[key] = {"_created": time.time()}

        self.data[key]["_updated"] = time.time()
        self.data[key]["_rev"] = self.data.get(key, {}).get("_rev", 0) + 1
        self.data[key].update(value)

        if self.replication_master:
            await self.update_data_on_master(key, value)

    async def delete(self, key: str):
        if key in self.data:
            del self.data[key]

        if self.replication_master:
            await self.delete_data_on_master(key)

    async def list_keys(self) -> List[str]:
        return list(self.data.keys())

    async def list_values(self) -> List[Any]:
        return list(self.data.values())

    async def create_index(self, column: str):
        for key, value in self.data.items():
            if column in value:
                await self.update_index_on_master(column, value[column], key)

        self.create_indexes()

    def create_indexes(self):
        self.indexes = {}

        for key, value in self.data.items():
            for column, val in value.items():
                if column not in self.indexes:
                    self.indexes[column] = {}

                if val not in self.indexes[column]:
                    self.indexes[column][val] = set()

                self.indexes[column][val].add(key)

    async def search_index(self, column: str, value: Any) -> List[str]:
        if self.replication_master:
            return await self.search_index_on_master(column, value)

        return [key for key, data in self.data.items() if data.get(column) == value]

    async def update_data_on_master(self, key: str, value: Any):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{self.replication_master}:{self.replication_master_port}/set",
                json={"key": key, "value": value},
            ) as response:
                pass

    async def delete_data_on_master(self, key: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{self.replication_master}:{self.replication_master_port}/delete",
                json={"key": key},
            ) as response:
                pass

    async def update_index_on_master(self, column: str, value: Any, key: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{self.replication_master}:{self.replication_master_port}/create_index",
                json={"column": column, "value": value, "key": key},
            ) as response:
                pass

    async def search_index_on_master(self, column: str, value: Any) -> List[str]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{self.replication_master}:{self.replication_master_port}/search_index",
                json={"column": column, "value": value},
            ) as response:
                result = await response.json()
                return result["keys"]
