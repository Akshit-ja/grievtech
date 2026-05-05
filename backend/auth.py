from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pre-generated hash (generate once and paste here)
ADMIN_HASH = "$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXX"

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": ADMIN_HASH,
        "role": "admin"
    }
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate(username: str, password: str):
    user = fake_users_db.get(username)

    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    return user