from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=3000,
)


def hash(password):
    return pwd_context.encrypt(password)


def check(password, hashed):
    return pwd_context.verify(password, hashed)
