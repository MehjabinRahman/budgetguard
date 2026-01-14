from typing import Optional
from .db import connect
from .utils import make_salt, hash_password

def register(username: str, password: str) -> bool:
    salt = make_salt()
    pw_hash = hash_password(password, salt)

    try:
        with connect() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, pw_hash, salt),
            )
        return True
    except Exception:
        return False

def login(username: str, password: str) -> Optional[int]:
    with connect() as conn:
        row = conn.execute(
            "SELECT id, password_hash, salt FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if not row:
        return None

    user_id, stored_hash, salt = row
    if hash_password(password, salt) == stored_hash:
        return user_id
    return None
