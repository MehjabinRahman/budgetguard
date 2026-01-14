import hashlib
import os

def make_salt() -> str:
    return os.urandom(16).hex()

def hash_password(password: str, salt: str) -> str:
    data = (salt + password).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
