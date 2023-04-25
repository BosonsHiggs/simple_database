import hashlib


def hash_string(string: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(string.encode("utf-8"))
    return sha256.hexdigest()
