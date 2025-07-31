# routers/product.py
from fastapi import APIRouter, Body, HTTPException, status, File, UploadFile
import aiofiles
import uuid
import os
from fastapi.responses import JSONResponse
from bson import ObjectId

from .. database import product_collection, product_helper
from .. models import ProductCreateModel, ProductUpdateModel

router = APIRouter()

IMAGE_DIR = "static/images/"

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreateModel = Body(...)):
    product_dict = product.dict()
    new_product = await product_collection.insert_one(product_dict)
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    return product_helper(created_product)

@router.get("/")
async def get_all_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products

@router.get("/{id}")
async def get_product_by_id(id: str):
    if (product := await product_collection.find_one({"_id": ObjectId(id)})) is not None:
        return product_helper(product)
    raise HTTPException(status_code=404, detail=f"Product {id} not found")

@router.put("/{id}")
async def update_product(id: str, product: ProductUpdateModel = Body(...)):
    product_data = {k: v for k, v in product.dict().items() if v is not None}
    if len(product_data) >= 1:
        update_result = await product_collection.update_one({"_id": ObjectId(id)}, {"$set": product_data})
        if update_result.modified_count == 1:
            if (updated_product := await product_collection.find_one({"_id": ObjectId(id)})) is not None:
                return product_helper(updated_product)
    if (existing_product := await product_collection.find_one({"_id": ObjectId(id)})) is not None:
        return product_helper(existing_product)
    raise HTTPException(status_code=404, detail=f"Product {id} not found")

# --- Endpoint ใหม่สำหรับอัปโหลดรูปภาพ ---
@router.post("/{id}/upload-image")
async def upload_product_image(id: str, file: UploadFile = File(...)):
    # ตรวจสอบว่ามีสินค้านี้อยู่จริงหรือไม่
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    # สร้างชื่อไฟล์ใหม่ที่ไม่ซ้ำกันโดยใช้ UUID เพื่อป้องกันการเขียนทับ
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(IMAGE_DIR, new_filename)

    # บันทึกไฟล์ลงใน disk แบบ async
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")

    # สร้าง URL ที่จะใช้เข้าถึงรูปภาพ
    image_url = f"/{file_path}"
    
    # อัปเดต path ของรูปภาพลงในฐานข้อมูล
    await product_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": {"image_url": image_url}}
    )
    
    # ดึงข้อมูลสินค้าที่อัปเดตแล้วกลับไป
    updated_product = await product_collection.find_one({"_id": ObjectId(id)})
    return product_helper(updated_product)


# --- แก้ไข Endpoint สำหรับลบสินค้า ---
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    # 1. ค้นหาสินค้าก่อนเพื่อเอา URL ของรูปภาพ
    product_to_delete = await product_collection.find_one({"_id": ObjectId(id)})
    
    if not product_to_delete:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    # 2. ลบไฟล์รูปภาพออกจาก disk (ถ้ามี)
    image_url = product_to_delete.get("image_url")
    if image_url:
        # ลบ / ที่ข้างหน้าออกเพื่อให้เป็น path ที่ถูกต้อง
        image_path = image_url.lstrip('/') 
        if os.path.exists(image_path):
            os.remove(image_path)
    
    # 3. ลบข้อมูลสินค้าออกจากฐานข้อมูล
    await product_collection.delete_one({"_id": ObjectId(id)})
    return