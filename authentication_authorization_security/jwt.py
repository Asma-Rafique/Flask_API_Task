from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt

secret_key = ""
algo = "HS256"
access_token_expire_date = 30

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algo)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algo])
        email: str = payload.get("sub")
        if email is None:
            return None
        return payload
    except JWTError:
        return None
