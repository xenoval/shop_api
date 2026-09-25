import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone

from config import settings


def get_password_hash(password: str) -> str:
    """Хеширует пароль с помощью bcrypt."""
    # bcrypt принимает только байты
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль против хеша."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except ValueError:
        # На случай, если хеш в базе повреждён или не является bcrypt-хешем
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings. SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Бросает jwt.PyJWTError, если токен невалиден или истек"""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])