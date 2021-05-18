from typing import List
from fastapi import APIRouter, HTTPException
from h11 import LocalProtocolError

from zadanie5.dbservice import get_db
from pydantic import PositiveInt
from sqlalchemy.orm import Session
from zadanie5 import schemas
from zadanie5 import crud

router = APIRouter()


@router.get("/test", status_code=200)
def get_test():
    return "Testyy ok"


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shipper():
    with get_db() as db:
        db_shipper = crud.get_all_shippers(db)
        if db_shipper is None:
            raise HTTPException(status_code=404, detail="Shipper not found")
        return db_shipper


@router.get("/countshippers")
async def count_shippers():
    with get_db() as db:
        return crud.get_shippers_count(db)


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers():
    with get_db() as connection:
        return crud.get_suppliers(connection)


@router.get("/suppliers/{supplierid}", response_model=schemas.Supplier)
async def get_supplier_byid(supplierid: int):
    with get_db() as connection:
        result = crud.get_supplier_by_id(connection, supplierid)
        if result is None:
            raise HTTPException(status_code=404, detail="Nie ma takiego dostawcy")
        return result


@router.get("/suppliers/{idsupplier}/products", status_code=200, response_model=List[schemas.SuppliersProduct])
async def get_supplier_products(idsupplier: int):
    with get_db() as connection:
        data = crud.get_supplier_products(connection, idsupplier=idsupplier)
        if data is None:
            raise HTTPException(status_code=404, detail="Nie ma takiego dostawcy")

        resultlist = list()
        for productid, name, discounted, category in data:
            wynik = schemas.SuppliersProduct(ProductID=productid, ProductName=name,
                                             Category=schemas.SimpleCategory.from_orm(category),
                                             Discounted=discounted
                                             )
            resultlist.append(wynik)
        return resultlist


@router.post("/suppliers", status_code=201, response_model=schemas.Supplier)
async def add_supplier(supplier: dict):
    with get_db() as connection:
        return crud.add_supplier(connection, supplier)


@router.put("/suppliers/{supplierid}", status_code=200)
async def update_supplier(supplier: dict, supplierid: int):

    validation = all(elem in schemas.Supplier.schema().get("properties") for elem in supplier.keys())
    if not validation:
        raise HTTPException(status_code=400, detail="Pola jakich być nie powinno")

    with get_db() as connection:
        result = crud.update_supplier(db=connection, supplier=supplier, supplierid=supplierid)
        if result is None:
            raise HTTPException(status_code=404, detail="Nie ma takiego suppliera")
        return result


@router.delete("/suppliers/{supplierid}", status_code=204)
async def delete_supplier(supplierid: int):
    with get_db() as connection:
        result = crud.delete_supplier(db=connection, supplierid=supplierid)
        if not result:
            raise HTTPException(status_code=404, detail="Nie ma juz")
        return None
