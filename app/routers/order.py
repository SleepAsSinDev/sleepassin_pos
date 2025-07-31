from fastapi import APIRouter, Body, HTTPException, status
from datetime import datetime
from bson import ObjectId

from database import product_collection, order_collection, order_helper
from models import OrderCreateModel, OrderStatusUpdateModel

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreateModel = Body(...)):
    order_items = []
    total_amount = 0.0
    for item in order_data.items:
        product = await product_collection.find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found.")
        options_price = sum(opt.price for opt in item.selected_options)
        price_per_unit = product["price"] + options_price
        item_total = price_per_unit * item.quantity
        total_amount += item_total
        order_items.append({
            "product_id": item.product_id,
            "product_name": product["name"],
            "quantity": item.quantity,
            "price_per_unit": price_per_unit,
            "selected_options": [opt.dict() for opt in item.selected_options],
            "item_total": item_total
        })
    new_order_data = {
        "items": order_items, "total_amount": total_amount,
        "status": "Pending", "order_date": datetime.utcnow()
    }
    result = await order_collection.insert_one(new_order_data)
    created_order = await order_collection.find_one({"_id": result.inserted_id})
    return order_helper(created_order)

@router.get("/")
async def get_all_orders():
    orders = []
    async for order in order_collection.find().sort("order_date", -1):
        orders.append(order_helper(order))
    return orders

@router.put("/{id}/status")
async def update_order_status(id: str, status_update: OrderStatusUpdateModel = Body(...)):
    update_result = await order_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": status_update.status}})
    if update_result.modified_count == 1:
        if (updated_order := await order_collection.find_one({"_id": ObjectId(id)})) is not None:
            return order_helper(updated_order)
    raise HTTPException(status_code=404, detail=f"Order {id} not found")