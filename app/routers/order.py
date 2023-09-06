from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/order",
    tags= ['Orders']
)
 
@router.post("/", status_code=status.HTTP_201_CREATED)
def place_order(order: schemas.OrderRequest, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product = db.query(models.Listing).filter(models.Listing.product_id == order.product_id).first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {order.product_id} does not exist")
    if order.quantity > product.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"the order quantity is more than available product quantity")
    cost = product.price * order.quantity
    new_order = models.Order(buyer_id=current_user.user_id, seller_id = product.user_id, cost = cost, **order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order  

@router.put("/{id}")
def change_order_status(id: int, order_status: schemas.OrderStatusChange, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    order_query = db.query(models.Order).filter(models.Order.order_id==id)
    order = order_query.first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders found")

    if order.seller_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login as seller to see your orders")

    updated_order = {
        "buyer_id": order.buyer_id,
        "seller_id": order.seller_id,
        "product_id": order.product_id, 
        "quantity": order.quantity,
        "cost": order.cost,
        "order_date": order.order_date,
        "status": order_status.status
        }
    order_query.update(updated_order, 
        synchronize_session=False)
    db.commit()
    return updated_order