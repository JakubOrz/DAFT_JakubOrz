from sqlalchemy import desc, func, update
from sqlalchemy.orm import Session

from zadanie5 import models2
from zadanie5 import schemas


def get_all_shippers(db: Session):
    return db.query(models2.Shipper).all()


def get_shippers_count(db: Session):
    return db.query(models2.Shipper).count()


def get_supplier_by_id(db: Session, idsupplier: int):
    return db.query(models2.Supplier).filter(models2.Supplier.SupplierID == idsupplier).first()


def get_suppliers(db: Session):
    return db.query(models2.Supplier).order_by(models2.Supplier.SupplierID).all()


def get_supplier_products(db: Session, idsupplier: int):
    tmp = db.query(models2.Supplier).filter(models2.Supplier.SupplierID == idsupplier).first()
    if tmp is None:
        return None

    return db.query(models2.Product) \
        .join(models2.Category, models2.Product.CategoryID == models2.Category.CategoryID) \
        .order_by(desc(models2.Product.ProductID)) \
        .filter(models2.Product.SupplierID == idsupplier).values(
        models2.Product.ProductID,
        models2.Product.ProductName,
        models2.Product.Discontinued,
        models2.Category
    )


def add_supplier(db: Session, supplier: dict):
    newid = int(db.query(func.max(models2.Supplier.SupplierID)).scalar()) + 1
    print(newid)

    newsupplier = models2.Supplier(**supplier)
    newsupplier.SupplierID = newid

    db.add(newsupplier)
    db.flush()
    db.commit()

    return db.query(models2.Supplier).filter(models2.Supplier.SupplierID == newid).first()


def update_supplier(db: Session, supplier: dict, supplierid: int):
    szukany = db.query(models2.Supplier).filter(models2.Supplier.SupplierID == supplierid)

    if szukany is None:
        return None

    szukany.update(supplier)
    db.commit()
    return db.query(models2.Supplier).filter(models2.Supplier.SupplierID == supplierid).first()


def delete_supplier(db: Session, supplierid: int) -> bool:
    szukany = db.query(models2.Supplier).filter(models2.Supplier.SupplierID == supplierid).first()
    if szukany is None:
        return False
    db.query(models2.Supplier).filter(models2.Supplier.SupplierID == supplierid).delete()
    db.commit()
    return True
