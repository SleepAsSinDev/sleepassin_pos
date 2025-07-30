# models.py
from pydantic import BaseModel, Field
from typing import Optional, List

# --- Product Models ---
class ProductCreateModel(BaseModel):
    name: str = Field(..., examples=["คาปูชิโน่ร้อน"])
    price: float = Field(..., examples=[60.0])
    category: str = Field(..., examples=["เครื่องดื่มร้อน"])

class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

# --- Order Models ---
class OrderItemCreateModel(BaseModel):
    product_id: str = Field(..., examples=["63e8a3c3f4a3d4e6c8f9b1d2"])
    quantity: int = Field(..., gt=0, examples=[2])

class OrderCreateModel(BaseModel):
    items: List[OrderItemCreateModel]

class OrderStatusUpdateModel(BaseModel):
    status: str = Field(..., examples=["Completed"])

class ProductCreateModel(BaseModel):
    name: str = Field(..., examples=["คาปูชิโน่ร้อน"])
    price: float = Field(..., examples=[60.0])
    category: str = Field(..., examples=["เครื่องดื่มร้อน"])
    # เพิ่ม image_url แต่เป็น optional เพราะอาจจะยังไม่มีรูปตอนสร้าง
    image_url: Optional[str] = Field(None, examples=["/static/images/latte.jpg"])

class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None