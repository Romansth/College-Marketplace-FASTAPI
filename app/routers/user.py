from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return user

@router.get("/{id}/listings", response_model=List[schemas.Listing])
def get_user_listings(id: int, db: Session = Depends(get_db)):
    listings = db.query(models.Listing).filter(models.Listing.user_id==id).all()

    if not listings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user listings for user id: {id} was not found")
    return listings

@router.get("/{id}/orders") #sellers to see their products
def get_user_orders(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    orders = db.query(models.Order).filter(models.Order.seller_id==id).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders found")

    if orders[0].seller_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login as seller to see your orders")

    return orders