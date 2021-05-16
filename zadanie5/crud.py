from sqlalchemy.orm import Session

from zadanie5 import models2


def get_all_shippers(db: Session):
    return db.query(models2.Shipper).all()


def get_shippers_count(db: Session):
    return db.query(models2.Shipper).count()


def get_suppliers(db: Session):
    return db.query(models2.Supplier).order_by(models2.Supplier.SupplierID).all()


