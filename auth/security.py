import bcrypt

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