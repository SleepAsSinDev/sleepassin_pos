# models.py (ฉบับอัปเดต)

from pydantic import BaseModel, Field
from typing import Optional, List

# --- โมเดลย่อยสำหรับ Options ---
class OptionChoice(BaseModel):
    name: str = Field(..., description="ชื่อของตัวเลือกย่อย", examples=["หวานน้อย (50%)", "ไข่มุก"])
    price: float = Field(..., description="ราคาที่บวกเพิ่มสำหรับตัวเลือกนี้ (ถ้าไม่มีคือ 0)", examples=[0, 10])

class ProductOption(BaseModel):
    name: str = Field(..., description="ชื่อกลุ่มของตัวเลือก", examples=["ระดับความหวาน", "ท็อปปิ้ง"])
    choices: List[OptionChoice]

# --- Product Models (อัปเดตแล้ว) ---
class ProductCreateModel(BaseModel):
    name: str = Field(..., examples=["ชานมไต้หวัน"])
    price: float = Field(..., examples=[45.0])
    category: str = Field(..., examples=["ชานม"])
    # เพิ่ม field ใหม่สำหรับเก็บตัวเลือกทั้งหมดของสินค้านี้
    options: List[ProductOption] = []

class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    options: Optional[List[ProductOption]] = None

# --- Order Models (อัปเดตแล้ว) ---
class OrderItemCreateModel(BaseModel):
    product_id: str = Field(..., examples=["63e8a3c3f4a3d4e6c8f9b1d2"])
    quantity: int = Field(..., gt=0, examples=[1])
    # เพิ่ม field ใหม่สำหรับเก็บตัวเลือกที่ลูกค้าเลือก
    selected_options: List[OptionChoice] = []

class OrderCreateModel(BaseModel):
    items: List[OrderItemCreateModel]

class OrderStatusUpdateModel(BaseModel):
    status: str = Field(..., examples=["Completed"])