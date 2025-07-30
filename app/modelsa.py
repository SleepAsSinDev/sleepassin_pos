# models.py
from pydantic import BaseModel, Field
from typing import Optional, List

# --- Product Models ---
class ProductCreateModel(BaseModel):
    name: str = Field(..., description="ชื่อสินค้า", examples=["คาปูชิโน่ร้อน"])
    price: float = Field(..., description="ราคา", examples=[60.0])
    category: str = Field(..., description="หมวดหมู่สินค้า", examples=["เครื่องดื่มร้อน"])

    class Config:
        json_schema_extra = { "example": { "name": "อเมริกาโน่เย็น", "price": 55.0, "category": "เครื่องดื่มเย็น" } }

class ProductUpdateModel(BaseModel):
    name: Optional[str] = Field(None, description="ชื่อสินค้า", examples=["อเมริกาโน่ (เมล็ดคั่วกลาง)"])
    price: Optional[float] = Field(None, description="ราคา", examples=[65.0])
    category: Optional[str] = Field(None, description="หมวดหมู่สินค้า")

    class Config:
        json_schema_extra = { "example": { "name": "อเมริกาโน่ (เมล็ดคั่วกลาง)", "price": 65.0 } }

# --- Order Models ---
class OrderItemCreateModel(BaseModel):
    product_id: str = Field(..., description="ID ของสินค้าจาก MongoDB", examples=["63e8a3c3f4a3d4e6c8f9b1d2"])
    quantity: int = Field(..., gt=0, description="จำนวนสินค้า", examples=[2])

class OrderCreateModel(BaseModel):
    items: List[OrderItemCreateModel]

class OrderStatusUpdateModel(BaseModel):
    status: str = Field(..., description="สถานะใหม่ของออเดอร์", examples=["Completed"])

# --- User & Auth Models ---
class UserCreateModel(BaseModel):
    username: str = Field(..., description="ชื่อผู้ใช้สำหรับเข้าระบบ")
    password: str = Field(..., description="รหัสผ่าน")
    role: str = Field("staff", description="บทบาทของผู้ใช้ (staff, admin)")

    class Config:
        json_schema_extra = { "example": { "username": "employee01", "password": "securepassword123", "role": "staff" } }

class User(BaseModel):
    id: str
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None