from pydantic import BaseModel, Field
from typing import Optional, List

class OptionChoice(BaseModel):
    name: str = Field(..., examples=["หวานน้อย (50%)", "ไข่มุก"])
    price: float = Field(..., examples=[0, 10])

class ProductOption(BaseModel):
    name: str = Field(..., examples=["ระดับความหวาน", "ท็อปปิ้ง"])
    choices: List[OptionChoice]

class ProductCreateModel(BaseModel):
    name: str = Field(..., examples=["ชานมไต้หวัน"])
    price: float = Field(..., examples=[45.0])
    category: str = Field(..., examples=["ชานม"])
    options: List[ProductOption] = []

class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    options: Optional[List[ProductOption]] = None

class OrderItemCreateModel(BaseModel):
    product_id: str = Field(..., examples=["63e8a3c3f4a3d4e6c8f9b1d2"])
    quantity: int = Field(..., gt=0, examples=[1])
    selected_options: List[OptionChoice] = []

class OrderCreateModel(BaseModel):
    items: List[OrderItemCreateModel]

class OrderStatusUpdateModel(BaseModel):
    status: str = Field(..., examples=["Completed"])