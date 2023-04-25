# Simple Database

A lightweight and simple database implementation in Python, designed for small-scale applications and projects. This implementation is not intended to replace established databases like MySQL, PostgreSQL, or MongoDB. Instead, it is aimed at providing basic database functionality for small projects where the overhead of setting up a full-fledged database is not required.

**Note**: This library is not recommended for high-traffic applications or projects that require advanced features, scalability, and fault tolerance provided by traditional database management systems.

## Features

- Simple key-value storage
- Support for integers, strings, JSON, and images
- Basic transaction support
- Query support with custom filter functions
- B-tree based storage for improved performance

# Estrutura do projeto:

```lua
simple_database/
|-- simple_database/
|   |-- __init__.py
|   |-- simple_database.py
|-- .gitignore
|-- README.md
|-- setup.py
```

## Installation

Install the package using pip:

```python
pip install -e .
```

# Usage

## Synchronous version
```python
from simple_database import SimpleDatabase

# Create a new database
db = SimpleDatabase("my_database")

# Insert data
db.insert_data("example_key_1", "example_value_1")
db.insert_data("example_key_2", 12345)
db.insert_data("example_key_3", {"key": "value"})

# Get data
print(db.get_data("example_key_1"))
print(db.get_data("example_key_2"))
print(db.get_data("example_key_3"))

# Query data
result = db.query(lambda k, v: k.startswith("example_key"))
print(result)

# Basic transactions
with db.transaction():
    db.insert_data("key1", "value1")
    db.insert_data("key2", "value2")

# Delete data
db.delete_data("example_key_1")
print(db.get_data("example_key_1"))
```
## Asynchronous version
```python
import asyncio
from simple_database import AsyncSimpleDatabase

async def main():
    db = AsyncSimpleDatabase("my_database")

    # Insert data
    await db.insert_data("example_key_1", "example_value_1")
    await db.insert_data("example_key_2", 12345)
    await db.insert_data("example_key_3", {"key": "value"})

    # Get data
    print(await db.get_data("example_key_1"))
    print(await db.get_data("example_key_2"))
    print(await db.get_data("example_key_3"))

    # Query data
    result = await db.query(lambda k, v: k.startswith("example_key"))
    print(result)

    # Basic transactions
    async with db.transaction():
        await db.insert_data("key1", "value1")
        await db.insert_data("key2", "value2")

    # Delete data
    await db.delete_data("example_key_1")
    print(await db.get_data("example_key_1"))

if __name__ == "__main__":
    asyncio.run(main())
```

# Contributing
Contributions to improve the library are welcome. Please submit a pull request or create an issue to discuss your ideas.

# License
This project is licensed under the MIT License.

