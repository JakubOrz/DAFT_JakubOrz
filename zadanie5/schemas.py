from typing import Optional
from zadanie5 import models2

from pydantic import BaseModel, PositiveInt, constr, NonNegativeInt


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class Supplier(BaseModel):
    SupplierID: Optional[PositiveInt]
    CompanyName: constr(max_length=40)
    ContactName: constr(max_length=30)
    ContactTitle: constr(max_length=30) = None
    Address: constr(max_length=60) = None
    City: constr(max_length=15) = None
    Region: constr(max_length=15) = None
    PostalCode: constr(max_length=10) = None
    Country: constr(max_length=15) = None
    Phone: constr(max_length=24) = None
    Fax: constr(max_length=24) = None
    HomePage: constr() = None

    class Config:
        orm_mode = True


class SimpleCategory(BaseModel):

    CategoryID: PositiveInt
    CategoryName: constr(max_length=15) = None

    class Meta:
        orm_model = models2.Category

    class Config:
        orm_mode = True


class SuppliersProduct(BaseModel):
    ProductID: PositiveInt
    ProductName: constr(max_length=40) = None
    Category: Optional[SimpleCategory]
    Discounted: Optional[NonNegativeInt]

    class Config:
        orm_mode = True



