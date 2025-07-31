from fastapi import APIRouter, Body, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse
from bson import ObjectId
import aiofiles
import uuid
import os

from database import product_collection, product_helper
from models import ProductCreateModel, ProductUpdateModel

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
    product_data = product.dict(exclude_unset=True)
    if len(product_data) >= 1:
        await product_collection.update_one({"_id": ObjectId(id)}, {"$set": product_data})
        if (updated_product := await product_collection.find_one({"_id": ObjectId(id)})) is not None:
            return product_helper(updated_product)
    raise HTTPException(status_code=404, detail=f"Product {id} not found")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    product_to_delete = await product_collection.find_one({"_id": ObjectId(id)})
    if not product_to_delete:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")
    image_url = product_to_delete.get("image_url")
    if image_url:
        image_path = image_url.lstrip('/')
        if os.path.exists(image_path):
            os.remove(image_path)
    await product_collection.delete_one({"_id": ObjectId(id)})
    return

@router.post("/{id}/upload-image")
async def upload_product_image(id: str, file: UploadFile = File(...)):
    if not await product_collection.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=404, detail=f"Product {id} not found")
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(IMAGE_DIR, new_filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    image_url = f"/{file_path}"
    await product_collection.update_one({"_id": ObjectId(id)}, {"$set": {"image_url": image_url}})
    updated_product = await product_collection.find_one({"_id": ObjectId(id)})
    return product_helper(updated_product)