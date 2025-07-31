import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.coffee_pos

product_collection = database.get_collection("products")
order_collection = database.get_collection("orders")

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "image_url": product.get("image_url"),
        "options": product.get("options", [])
    }

def order_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "items": order["items"],
        "total_amount": order["total_amount"],
        "status": order["status"],
        "order_date": str(order["order_date"])
    }