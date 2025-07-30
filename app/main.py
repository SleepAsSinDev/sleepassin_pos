# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . routers.product import router as product_router
from . routers.order import router as order_router

app = FastAPI(
    title="Sleep As Sin POS API",
    description="API สำหรับจัดการสินค้าและออเดอร์ (ไม่มีระบบยืนยันตัวตน)"
)

# นี่คือการบอกว่า URL path ที่ขึ้นต้นด้วย "/static" 
# ให้ไปหาไฟล์จาก directory ที่ชื่อว่า "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# เพิ่ม Router สำหรับสินค้าและออเดอร์
app.include_router(product_router, tags=["Products"], prefix="/products")
app.include_router(order_router, tags=["Orders"], prefix="/orders")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Sleep As Sin POS API!"}