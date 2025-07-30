# routers/auth.py
from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from autha import (ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,
                  get_password_hash, verify_password)
from databasea import user_collection
from modelsa import Token, UserCreateModel

router = APIRouter()

@router.post("/register", response_description="Register a new user", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateModel = Body(...)):
    if await user_collection.find_one({"username": user_data.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(user_data.password)
    user_object = {"username": user_data.username, "hashed_password": hashed_password, "role": user_data.role}
    await user_collection.insert_one(user_object)
    return {"message": f"User {user_data.username} created successfully."}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user.get("role")}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}