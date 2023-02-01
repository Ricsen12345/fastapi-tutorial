from passlib.context import CryptContext

# Hashing password (encryption)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(unhashedData, hashedData):
    return pwd_context.verify(unhashedData, hashedData)