# database.py
import motor.motor_asyncio

# Connection String แบบไม่ต้องใช้รหัสผ่าน
MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.coffee_pos

# ไม่ต้องมี user_collection อีกต่อไป
product_collection = database.get_collection("products")
order_collection = database.get_collection("orders")


# Helper functions เพื่อแปลงข้อมูล
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
        "order_date": str(order["order_date"])
    }

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        # เพิ่มการดึง image_url, ถ้าไม่มีให้เป็น None
        "image_url": product.get("image_url") 
    }