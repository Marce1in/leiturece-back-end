from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_secret(hash_secret: str, secret: str) -> bool:
    return passwd_context.verify(secret, hash_secret)


def hash_secret(secret: str) -> str:
    return passwd_context.hash(secret)
