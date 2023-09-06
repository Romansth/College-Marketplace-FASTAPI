from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    class_year: int

class UserCreate(UserBase):
    pass

class UserOut(BaseModel): #response schema
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    class_year: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ListingBase(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    condition: str

class ListingCreate(ListingBase):
    pass

class Listing(ListingBase): #response schema
    date_posted: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None