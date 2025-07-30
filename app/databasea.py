# database.py
import motor.motor_asyncio
from bson import ObjectId

# URL สำหรับเชื่อมต่อ MongoDB
MONGO_DETAILS = "mongodb://192.168.1.145:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# เลือกฐานข้อมูล
database = client.coffee_pos

# เตรียม Collections ที่จะใช้
product_collection = database.get_collection("products")
order_collection = database.get_collection("orders")
user_collection = database.get_collection("users")


# Helper functions เพื่อแปลงข้อมูลจาก MongoDB ObjectId
def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
    }

def order_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "items": order["items"],
        "total_amount": order["total_amount"],
        "status": order["status"],
        "order_date": order["order_date"]
    }

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user.get("role")
    }