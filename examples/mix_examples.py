from simple_database.async_simple_database import AsyncSimpleDatabase
from simple_database.simple_database import SimpleDatabase


async def run_async():
    # criando instância assíncrona do banco de dados
    async_db = AsyncSimpleDatabase()

    # escrevendo valores assincronamente
    await async_db.set("key1", "value1")
    await async_db.set("key2", "value2")

    # lendo valores síncronamente
    db = SimpleDatabase()
    print(db.get("key1"))
    print(db.get("key2"))

    # lendo valores assincronamente
    print(await async_db.get("key1"))
    print(await async_db.get("key2"))


# executando a função assíncrona
asyncio.run(run_async())
