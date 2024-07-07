from fastapi import APIRouter, HTTPException, status
from models.user import User, UserLogin
from config.db import conn
# from schemas.user import serializeDict, serializeList
from schemas.user import usersEntity, userEntity
from bson import ObjectId
from authentication_authorization_security.security import verify_password, hash_password
from authentication_authorization_security.jwt import create_access_token, timedelta, access_token_expire_date
user = APIRouter()


@user.get('/')
async def find_all_users():
    # print(conn.user.user.find())
    # print(usersEntity(conn.user.user.find()))
    return usersEntity(conn.user.user.find())

    # return serializeList(conn.user.user.find())

# @user.get('/{id}')
# async def find_one_user(id):
#     return serializeDict(conn.user.user.find_one({"_id":ObjectId(id)}))


@user.post('/register')
async def create_user(user: User):
    if conn.user.user.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Hash the password before storing
    user.password = hash_password(user.password)
    conn.user.user.insert_one(dict(user))
    return {"msg": " User created successfully"}


@user.post('/login')
async def login(user: UserLogin):
    db_user = conn.user.user.find_one({"email": user.email})
    print("User found:", db_user)
    if not db_user or not verify_password(user.password, db_user['password']):
        print("Password verification failed")  # Debug print
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_date)
    access_token = create_access_token(
        data={"sub": db_user["email"]}, expires_delta=access_token_expires
    )
    return {"login": "successful", "access_token": access_token, "token_type": "bearer"}


@user.put('/{name}')
async def update_user(name, user: User):
    conn.user.user.find_one_and_update({"name": ObjectId(name)}, {
        "$set": dict(user)
    })
    return usersEntity(conn.user.user.find_one({"name": ObjectId(name)}))


@user.delete('/{id}')
async def delete_user(id, user: User):
    return usersEntity(conn.user.user.find_one_and_delete({"_id": ObjectId(id)}))
