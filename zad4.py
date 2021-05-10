# import sqlite3
import aiosqlite
from fastapi import APIRouter, HTTPException

zad4ruter = APIRouter()


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
async def get_employees(limit: int, offset: int, order: str = "id"):
    if order not in ["id", "last_name", "first_name", "city"]:
        raise HTTPException(status_code=400, detail="Niepoprawny parametr order")

    orderowanie = {
        'id': 'EmployeeID',
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'city': 'City'
    }
    command = f"SELECT EmployeeID, LastName, FirstName, City " \
              "FROM employees" \
              " ORDER BY " + str(orderowanie.get(order)) + "" \
                                                           " LIMIT :limit" \
                                                           " OFFSET :offsetting"
    params = {'orderowanie': order, 'limit': limit, 'offsetting': offset}

    cursor = await zad4ruter.connection.execute(command, params)
    data = await cursor.fetchall()
    if data is None:
        raise HTTPException(status_code=404, detail="Nie ma takiego pracownika")
    result = [{"id": x['EmployeeID'], "last_name": x['LastName'],
               "first_name": x['FirstName'], "city": x['City']} for x in data]
    return {"employees": result}