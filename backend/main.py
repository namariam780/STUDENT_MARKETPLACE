from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI(
    title="Student Marketplace API",
    description="Backend API for the Student Marketplace",
    version="1.0.0"
)


class ProductCreate(BaseModel):
    name: str
    category_id: int
    price: float
    seller_id: int


@app.get("/")
def home():
    return {"message": "Welcome to the Student Marketplace API"}


@app.get("/health")
def health():
    return {"status": "API is running"}


@app.get("/products")
def get_products():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        return products
    finally:
        cursor.close()
        connection.close()


@app.get("/products/{product_id}")
def get_product(product_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM product WHERE product_id = %s",
            (product_id,)
        )
        product = cursor.fetchone()

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product
    finally:
        cursor.close()
        connection.close()

@app.put("/products/{product_id}")
def update_product(product_id: int, product: dict):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE product
            SET category_id = %s, name = %s, price = %s,
                seller_id = %s
            WHERE product_id = %s
            """,
            (
                product["category_id"],
                product["name"],
                product["price"],
                product["seller_id"],
                product_id
            )
        )

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT product_id FROM product WHERE product_id = %s",
                (product_id,)
            )
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )

        connection.commit()
        return {"message": "Product updated successfully"}

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
@app.post("/products")
def create_product(product: ProductCreate):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """INSERT INTO product
            (name, category_id, price, seller_id)
            VALUES (%s, %s, %s, %s)""",
            (
                product.name,
                product.category_id,
                product.price,
                product.seller_id
            )
        )

        connection.commit()

        return {
            "message": "Product created successfully",
            "product_id": cursor.lastrowid
        }
    finally:
        cursor.close()
        connection.close()

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM product WHERE product_id = %s",
            (product_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        connection.commit()

        return {"message": "Product deleted successfully"}

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

@app.get("/students")
def get_students():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT student_id, name, email, phone_number FROM student")
        students = cursor.fetchall()
        return students

    finally:
        cursor.close()
        connection.close()

@app.post("/students")
def add_student(student: dict):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        
        cursor.execute("SELECT DATABASE()")
        print("DATABASE USED:", cursor.fetchone())

        cursor.execute("SHOW COLUMNS FROM student")
        print("COLUMNS FOUND:", [row[0] for row in cursor.fetchall()])
        cursor.execute(
            """
            INSERT INTO student (name, email, phone_number, password)
            VALUES (%s, %s, %s, %s)
            """,
            (
                student["name"],
                student["email"],
                student["phone_number"],
                student["password"]
            )
        )

        connection.commit()
        return {"message": "Student added successfully"}

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

@app.get("/categories")
def get_categories():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        return categories

    finally:
        cursor.close()
        connection.close()
       
@app.post("/categories")
def add_category(category: dict):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO category (category_name) VALUES (%s)",
            (category["category_name"],)
        )

        connection.commit()
        return {"message": "Category added successfully"}

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

@app.get("/orders")
def get_orders():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        return orders

    finally:
        cursor.close()
        connection.close()

@app.post("/orders")
def add_order(order: dict):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO orders (buyers_id, order_date, total_amount)
            VALUES (%s, %s, %s)
            """,
            (
                order["buyers_id"],
                order["order_date"],
                order["total_amount"]
            )
        )

        connection.commit()
        return {"message": "Order added successfully"}

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
        
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM orders WHERE order_id = %s",
            (order_id,)
        )

        order = cursor.fetchone()

        if order is None:
            return {"message": "Order not found"}

        return order

    finally:
        cursor.close()
        connection.close()

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM orders WHERE order_id = %s",
            (order_id,)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {"message": "Order not found"}

        return {"message": "Order deleted successfully"}

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
@app.put("/orders/{order_id}")
def update_order(order_id: int, order: dict):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE orders
            SET buyers_id = %s,
                order_date = %s,
                total_amount = %s
            WHERE order_id = %s
            """,
            (
                order["buyers_id"],
                order["order_date"],
                order["total_amount"],
                order_id
            )
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {"message": "Order not found or unchanged"}

        return {"message": "Order updated successfully"}

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
       
@app.post("/order-items")
def add_order_item(item: dict):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT price FROM product WHERE product_id = %s",
            (item["product_id"],)
        )
        product = cursor.fetchone()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute(
            "SELECT order_id FROM orders WHERE order_id = %s",
            (item["order_id"],)
        )
        order = cursor.fetchone()

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        quantity = item["quantity"]

        if quantity < 1:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be at least 1"
            )

        unit_price = product["price"]

        cursor.execute(
            """
            INSERT INTO order_items
                (order_id, product_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            """,
            (
                item["order_id"],
                item["product_id"],
                quantity,
                unit_price
            )
        )

        cursor.execute(
            """
            SELECT COALESCE(SUM(quantity * unit_price), 0) AS total
            FROM order_items
            WHERE order_id = %s
            """,
            (item["order_id"],)
        )
        total = cursor.fetchone()["total"]

        cursor.execute(
            """
            UPDATE orders
            SET total_amount = %s
            WHERE order_id = %s
            """,
            (total, item["order_id"])
        )

        connection.commit()

        return {
            "message": "Product added to order successfully",
            "order_id": item["order_id"],
            "product_id": item["product_id"],
            "quantity": quantity,
            "unit_price": str(unit_price),
            "total_amount": str(total)
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

@app.get("/order-items")
def get_order_items():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM order_items")
        items = cursor.fetchall()
        return items

    finally:
        cursor.close()
        connection.close()