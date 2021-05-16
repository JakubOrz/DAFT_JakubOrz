from typing import List
from fastapi import APIRouter, HTTPException
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


@router.get("/suppliers")
async def get_suppliers():
    with get_db() as connection:
        return crud.get_suppliers(connection)
