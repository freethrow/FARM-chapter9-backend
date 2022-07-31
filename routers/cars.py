from math import ceil

from typing import List, Optional

from fastapi import APIRouter, Request, Body, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder


from models import CarBase

from utils.report import report_pipeline


router = APIRouter()


@router.get("/", response_description="List all cars")
async def list_all_cars(
    request: Request,
    min_price: int = 0,
    max_price: int = 100000,
    brand: Optional[str] = None,
    page: int = 1,
) -> List[CarBase]:

    RESULTS_PER_PAGE = 25
    skip = (page - 1) * RESULTS_PER_PAGE

    query = {"price": {"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand

    # count total docs
    pages = ceil(
        await request.app.mongodb["cars"].count_documents(query) / RESULTS_PER_PAGE
    )

    full_query = (
        request.app.mongodb["cars"]
        .find(query)
        .sort("km", -1)
        .skip(skip)
        .limit(RESULTS_PER_PAGE)
    )

    results = [CarBase(**raw_car) async for raw_car in full_query]

    return {"results": results, "pages": pages}


# sample of N cars
@router.get("/sample/{n}", response_description="Sample of N cars")
async def get_sample(n: int, request: Request):

    query = [
        {"$match": {"year": {"$gt": 2010}}},
        {
            "$project": {
                "_id": 0,
            }
        },
        {"$sample": {"size": n}},
        {"$sort": {"brand": 1, "make": 1, "year": 1}},
    ]

    full_query = request.app.mongodb["cars"].aggregate(query)
    results = [el async for el in full_query]
    return results


# aggregation by model / avg price
@router.get("/brand/{val}/{brand}", response_description="Get brand models by val")
async def brand_price(brand: str, val: str, request: Request):

    query = [
        {"$match": {"brand": brand}},
        {"$project": {"_id": 0}},
        {
            "$group": {"_id": {"model": "$make"}, f"avg_{val}": {"$avg": f"${val}"}},
        },
        {"$sort": {f"avg_{val}": 1}},
    ]

    full_query = request.app.mongodb["cars"].aggregate(query)
    return [el async for el in full_query]


# count cars by brand
@router.get("/brand/count", response_description="Count by brand")
async def brand_count(request: Request):

    query = [{"$group": {"_id": "$brand", "count": {"$sum": 1}}}]

    full_query = request.app.mongodb["cars"].aggregate(query)
    return [el async for el in full_query]


# count cars by make
@router.get("/make/count/{brand}", response_description="Count by brand")
async def brand_count(brand: str, request: Request):

    query = [
        {"$match": {"brand": brand}},
        {"$group": {"_id": "$make", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]

    full_query = request.app.mongodb["cars"].aggregate(query)
    results = [el async for el in full_query]
    return results


# get car by ID
@router.get("/{id}", response_description="Get a single car")
async def show_car(id: str, request: Request):
    if (car := await request.app.mongodb["cars"].find_one({"_id": id})) is not None:
        return CarBase(**car)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.post("/email", response_description="Send email")
async def send_mail(
    background_tasks: BackgroundTasks,
    cars_num: int = Body(...),
    email: str = Body(...),
):
    print(email, cars_num)
    print("Sending report in the background")
    background_tasks.add_task(report_pipeline, email, cars_num)

    return {"Received": {"email": email, "cars_num": cars_num}}
