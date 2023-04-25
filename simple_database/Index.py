from typing import Any, Dict, List


index: Dict[Any, List[str]] = {}


def create_index(data: Dict[str, Any], column: str):
    global index
    index = {}

    for key, value in data.items():
        if column in value:
            if value[column] not in index:
                index[value[column]] = []

            index[value[column]].append(key)


def search_index(data: Dict[str, Any], column: str, value: Any) -> List[str]:
    global index

    if value in index:
        return index[value]

    return []
