from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)





SECRET_KEY="supersecret"

ALGORITHM="HS256"

def create_access_token(data):
    expire = datetime.utcnow() + timedelta(days=1)

    payload = data.copy()
    payload.update({"exp":expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_password(password,hashed):
    return pwd_context.verify(password,hashed)

def verify_token(token):
     try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
     except JWTError:
         return None