from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.hash import password_hash, verify_password
from utils.toks import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from utils import oauth2
from fastapi.responses import FileResponse


import schemas
import models
import database

getdb = database.getdb
router = APIRouter(tags=["user-space ;)"])


@router.get('/users', response_model=list[schemas.ShowUser], description="FUN-FACT: SHAMMAH MAKES GOOD MUSIC - JAH-MAN WAS")
def list_users(db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users


@router.get("/user/{id}", response_model=schemas.ShowUser, description="LOOKING FOR SOMEONE? WE'RE HERE TO HELP - INPUT THE USER-ID AND BOOM!")
def get_profile_by_id(id: int, db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="sorry, user not found. do try again :)")

    return user


@router.post("/user", response_model=schemas.ShowUser, description="WANNA JOIN THE FAMILY? HURRY UP! MAKE SURE YOU HAVE A UNIQUE NAME lol")
def sign_up_now(req: schemas.RegisterUser, db: Session = Depends(getdb)):
    user = db.query(models.User).filter(
        models.User.username == req.username).first()
    new_user = models.User(username=req.username, email=req.email,
                           password=password_hash(req.password))

    if user:
        raise HTTPException(
            status_code=404, detail="sorry, user already exists :)")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", description="MISS US MUCH?")
def sign_in(req: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getdb)):

    user = db.query(models.User).filter(
        models.User.username == req.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="user does not exist")

    if not verify_password(req.password, user.password):
        raise HTTPException(status_code=404, detail="user does not exist")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "message": "success!"}


@router.put("/profile/{id}", response_model=schemas.ShowBlog, description="NOBODY'S WATCHING, MAKE A CHANGE")
def edit_your_profile(req: schemas.UpdateUser, id: int, db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)

    if not id:
        raise HTTPException(
            status_code=404, detail="login to edit your profile :)")

    user.update(req.dict())

    db.commit()

    raise HTTPException(
        status_code=404, detail="change success :)")


@router.delete("/user/{id}", description="BUT WHY? ABEG WHY?")
def delete_user_account(id: int, db: Session = Depends(getdb), current_user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        return {"user does not exist, try again :("}

    user.delete()

    db.commit()

    return {"user deleted successfully :)"}
