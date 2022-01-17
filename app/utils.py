from passlib.context import CryptContext
pwc_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwc_context.hash(password)


def verify(plain_password, hashed_password):
    return pwc_context.verify(plain_password, hashed_password)
