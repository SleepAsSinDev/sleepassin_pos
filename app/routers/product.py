# routers/product.py
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from bson import ObjectId
from databasea import product_collection, product_helper
from modelsa import ProductCreateModel, ProductUpdateModel, User
from autha import get_current_user

router = APIRouter()

@router.post("/", response_description="Add new product", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreateModel = Body(...), current_user: User = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    
    product_dict = product.dict()
    new_product = await product_collection.insert_one(product_dict)
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=product_helper(created_product))

@router.get("/", response_description="List all products")
async def get_all_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products

@router.get("/{id}", response_description="Get a single product")
async def get_product_by_id(id: str):
    try:
        if (product := await product_collection.find_one({"_id": ObjectId(id)})) is not None:
            return product_helper(product)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")

@router.put("/{id}", response_description="Update a product")
async def update_product(id: str, product: ProductUpdateModel = Body(...), current_user: User = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    
    product_data = {k: v for k, v in product.dict().items() if v is not None}
    if len(product_data) >= 1:
        try:
            update_result = await product_collection.update_one({"_id": ObjectId(id)}, {"$set": product_data})
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        if update_result.modified_count == 1:
            if (updated_product := await product_collection.find_one({"_id": ObjectId(id)})) is not None:
                return product_helper(updated_product)
    if (existing_product := await product_collection.find_one({"_id": ObjectId(id)})) is not None:
        return product_helper(existing_product)
    raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")

@router.delete("/{id}", response_description="Delete a product")
async def delete_product(id: str, current_user: User = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    try:
        delete_result = await product_collection.delete_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Product successfully deleted"})
    raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")