# main.py
from fastapi import FastAPI
from .routers.product import router as product_router
from .routers.order import router as order_router
from .routers.auth import router as auth_router

app = FastAPI(
    title="Sleep As Sin POS API",
    description="API สำหรับระบบ Point of Sale ของ Sleep As Sin",
    version="1.0.0",
)

# เพิ่ม Router สำหรับการยืนยันตัวตน
app.include_router(auth_router, tags=["Authentication"], prefix="/auth")

# เพิ่ม Router สำหรับการจัดการสินค้า (ป้องกันโดย Authentication)
app.include_router(product_router, tags=["Products"], prefix="/products")

# เพิ่ม Router สำหรับการจัดการคำสั่งซื้อ (ป้องกันโดย Authentication)
app.include_router(order_router, tags=["Orders"], prefix="/orders")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Coffee POS API!"}