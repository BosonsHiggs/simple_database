import json
import base64
import asyncio
from typing import Any, Callable, Dict
from io import BytesIO
from PIL import Image
from blist import sorteddict
from contextlib import asynccontextmanager
import threading

class AsyncSimpleDatabase:
    def __init__(self, db_name: str, shard_count: int = 1):
        self.db_name = db_name
        self.shard_count = shard_count
        self.data = sorteddict()
        self.locks = [asyncio.Lock() for _ in range(shard_count)]
        self._cache = {}

    def _get_shard_name(self, key: str) -> str:
        return f"{self.db_name}_shard_{hash(key) % self.shard_count}.json"

    def _load_database(self):
        self.data = sorteddict()
        for shard_id in range(self.shard_count):
            shard_name = f"{self.db_name}_shard_{shard_id}.json"
            try:
                with open(shard_name, 'r') as f:
                    self.data.update(json.loads(f.read()))
            except FileNotFoundError:
                pass

    async def _save_database(self, shard_name: str):
        shard_data = {k: v for k, v in self.data.items() if self._get_shard_name(k) == shard_name}
        async with aiofiles.open(shard_name, 'w') as f:
            await f.write(json.dumps(shard_data))

    def _encode_data(self, data: Any) -> str:
        if isinstance(data, Image.Image):
            buffered = BytesIO()
            data.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        else:
            return json.dumps(data)

    def _decode_data(self, data: str) -> Any:
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            try:
                return Image.open(BytesIO(base64.b64decode(data)))
            except Exception:
                return data

    async def insert_data(self, key: str, value: Any):
        shard_name = self._get_shard_name(key)
        lock = self.locks[hash(key) % self.shard_count]
        async with lock:
            self.data[key] = self._encode_data(value)
            self._cache.clear()
            await self._save_database(shard_name)

    async def get_data(self, key: str) -> Any:
        if key in self._cache:
            return self._cache[key]

        value = self.data.get(key)
        if value is not None:
            decoded_value = self._decode_data(value)
            self._cache[key] = decoded_value
            return decoded_value
        return None

    async def delete_data(self, key: str):
        shard_name = self._get_shard_name(key)
        lock = self.locks[hash(key) % self.shard_count]
        async with lock:
            if key in self.data:
                del self.data[key]
                self._cache.clear()
                await self._save_database(shard_name)

    async def query(self, filter_func: Callable[[
