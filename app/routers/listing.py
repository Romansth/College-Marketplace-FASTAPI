from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/listings",
    tags= ['Listings']
)

@router.get("/", response_model=List[schemas.Listing])
def get_listings(db: Session = Depends(get_db), search: Optional[str] = ""):
    listings = db.query(models.Listing).filter(models.Listing.name.contains(search)).all()
    return listings
 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Listing)
def create_listings(listing: schemas.ListingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_listing = models.Listing(user_id=current_user.user_id, **listing.dict())
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing  

@router.get("/{id}", response_model=schemas.Listing)
def get_listing(id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.product_id == id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return listing

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_listing_query = db.query(models.Listing).filter(models.Listing.product_id == id)

    if deleted_listing_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if deleted_listing_query.first().user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    deleted_listing_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Listing)
def update_listing(id: int, listing: schemas.ListingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_listing_query = db.query(models.Listing).filter(models.Listing.product_id == id)
    updated_listing = updated_listing_query.first()
    if updated_listing == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if updated_listing.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
        
    updated_listing_query.update(listing.dict(), synchronize_session=False)
    db.commit()
    return updated_listing_query.first()
