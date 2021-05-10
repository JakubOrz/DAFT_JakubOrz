# import sqlite3
import aiosqlite
from fastapi import APIRouter, HTTPException

zad4ruter = APIRouter()
logger = list()


@zad4ruter.on_event("startup")
async def startup():
    zad4ruter.connection = await aiosqlite.connect("northwind.db")
    zad4ruter.connection.text_factory = lambda b: b.decode(errors="ignore")
    zad4ruter.connection.row_factory = aiosqlite.Row


@zad4ruter.on_event("shutdown")
async def shutdown():
    await zad4ruter.connection.close()


@zad4ruter.get("/testdb", status_code=200)
async def testybazy():
    cursor = await zad4ruter.connection.cursor()
    products = await cursor.execute("SELECT ProductName FROM Products").fetchall()
    return {
        "products": products,
    }


@zad4ruter.get("/categories", status_code=200)
async def get_categories():
    cursor = await zad4ruter.connection.execute("SELECT CategoryID, CategoryName FROM Categories")
    data = await cursor.fetchall()
    categories = [{"id": x['CategoryID'], "name": x['CategoryName']} for x in data]
    return {
        "categories": categories,
    }


@zad4ruter.get("/customers", status_code=200)
async def get_customers():
    cursor = await zad4ruter.connection.execute("SELECT CustomerID, CompanyName FROM Customers ORDER BY CustomerID")
    data = await cursor.fetchall()
    categories = [{"id": x['CustomerID'], "name": x['CompanyName']} for x in data]
    return {
        "customers": categories,
    }


@zad4ruter.get("/products/{id}")
async def get_single_customer(id: int):
    command = "SELECT ProductID, ProductName FROM Products WHERE ProductID = :prodid"
    params = {'prodid': id}
    cursor = await zad4ruter.connection.execute(command, params)
    data = await cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail="Nie ma takiego produktu")
    return {"id": data['ProductID'], "name": data['ProductName']}


@zad4ruter.get("/employees", status_code=200)
async def get_employees(limit: int = -1, offset: int = 0, order: str = "id"):
    logger.append(f"get employees {limit=} {offset=} {order=}")

    orderowanie = {
        'id': 'EmployeeID',
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'city': 'City'
    }

    if order not in orderowanie.keys():
        raise HTTPException(status_code=400, detail="Niepoprawny parametr order")

    command = f"SELECT EmployeeID, LastName, FirstName, City " \
              "FROM employees" \
              " ORDER BY " + str(orderowanie.get(order)) + "" \
                                                           " LIMIT :limit OFFSET :offsetting"
    params = {'orderowanie': order, 'limit': limit, 'offsetting': offset}

    cursor = await zad4ruter.connection.execute(command, params)
    data = await cursor.fetchall()
    if data is None:
        raise HTTPException(status_code=404, detail="Nie ma takiego pracownika")
    result = [{"id": x['EmployeeID'], "last_name": x['LastName'],
               "first_name": x['FirstName'], "city": x['City']} for x in data]
    return {"employees": result}


@zad4ruter.get("/products_extended", status_code=200)
async def get_products_extended():

    command = f"SELECT ProductID, ProductName, CategoryName, CompanyName" \
              f" FROM Products" \
              f" INNER JOIN Categories ON Categories.CategoryID = Products.CategoryID" \
              f" INNER JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID"

    cursor = await zad4ruter.connection.execute(command)
    data = await cursor.fetchall()
    result = [{"id": x['ProductID'], "name":x['ProductName'],
               "category":x['CategoryName'], "supplier":x['CompanyName']} for x in data]

    return {"products_extended": result}


@zad4ruter.get("/products/{id}/orders", status_code=200)
async def get_all_product_orders(id: int):
    command = f"SELECT c.CompanyName, od.UnitPrice, od.Quantity, od.Discount, o.OrderID " \
              f"FROM Products p" \
              f" INNER JOIN 'Order Details' od ON od.ProductID = p.ProductID" \
              f" INNER JOIN Orders o ON o.OrderID = od.OrderID" \
              f" INNER JOIN Customers c ON c.CustomerID = o.CustomerID" \
              f" WHERE p.ProductID = :productID"
    params = {"productID": id}

    cursor = await zad4ruter.connection.execute(command, params)
    data = await cursor.fetchall()
    if data is None:
        raise HTTPException(status_code=404, detail="Produktu o podanym id nie ma")
    orders = [{"id": x['OrderID'], "customer": x['CompanyName'], "quantity":x['Quantity'],
               "total_price":round((1 - float(x['Discount']))*(float(x['UnitPrice']) * int(x['Quantity'])), 2)}
              for x in data]
    return {"orders": orders}


@zad4ruter.get("/getlogs")
def getlogs():
    return logger
