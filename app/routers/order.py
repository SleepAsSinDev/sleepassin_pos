# routers/order.py
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
from bson import ObjectId

from database import product_collection, order_collection, order_helper
from models import OrderCreateModel, OrderStatusUpdateModel, User
from auth import get_current_user

router = APIRouter()

@router.post("/", response_description="Create a new order", status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreateModel = Body(...), current_user: User = Depends(get_current_user)):
    order_items = []
    total_amount = 0.0

    for item in order_data.items:
        product = await product_collection.find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {item.product_id} not found.")
        
        item_total = product["price"] * item.quantity
        total_amount += item_total
        
        order_items.append({
            "product_id": item.product_id, "product_name": product["name"],
            "price_per_item": product["price"], "quantity": item.quantity,
            "item_total": item_total
        })

    new_order_data = {
        "items": order_items, "total_amount": total_amount,
        "status": "Pending", "order_date": datetime.utcnow()
    }

    result = await order_collection.insert_one(new_order_data)
    created_order = await order_collection.find_one({"_id": result.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=order_helper(created_order))

@router.get("/", response_description="List all orders")
async def get_all_orders(current_user: User = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    orders = []
    async for order in order_collection.find().sort("order_date", -1):
        orders.append(order_helper(order))
    return orders

@router.get("/{id}", response_description="Get a single order")
async def get_order_by_id(id: str, current_user: User = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    try:
        if (order := await order_collection.find_one({"_id": ObjectId(id)})) is not None:
            return order_helper(order)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    raise HTTPException(status_code=404, detail=f"Order with ID {id} not found")

@router.put("/{id}/status", response_description="Update order status")
async def update_order_status(id: str, status_update: OrderStatusUpdateModel = Body(...), current_user: User = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    try:
        update_result = await order_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": status_update.status}})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    if update_result.modified_count == 1:
        if (updated_order := await order_collection.find_one({"_id": ObjectId(id)})) is not None:
            return order_helper(updated_order)
    raise HTTPException(status_code=404, detail=f"Order with ID {id} not found or status was not changed")