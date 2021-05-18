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
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)]
    HomePage: Optional[constr()]

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
    Discontinued: Optional[NonNegativeInt]

    class Config:
        orm_mode = True



