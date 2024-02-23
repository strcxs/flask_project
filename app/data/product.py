import uuid
import base64
from sqlalchemy import (
    insert,
    select,
    delete,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images


def get_category(title):
    q = run_query(
        select(Categories.id).where(
            Categories.title==title,
            Categories.status=="available"
        )
    )
    return q[0]["id"]


def get_image(image_name):
    image_file = open(f"/app/public/images/{image_name}", "rb")
    bs64_str = base64.b64encode(image_file.read())
    return f"base64,{bs64_str.decode('utf-8')}"


def product_dummy():
    data = [
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Greenlight T-shirt",
            "price": 60000,
            "condition": "used",
            "images": get_image("OIP (2).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Kaos polos hitam",
            "price": 35000,
            "condition": "new",
            "images": get_image("download (1).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Kaos roblox hitam",
            "price": 75000,
            "condition": "new",
            "images": get_image("download.jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Kaos polos merah",
            "price": 85000,
            "condition": "new",
            "images": get_image("OIP (1).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Kaos polos putih",
            "price": 50000,
            "condition": "new",
            "images": get_image("OIP.jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Armani exchange T-shirt",
            "price": 95000,
            "condition": "used",
            "images": get_image("download (3).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Kaos japan black",
            "price": 60000,
            "condition": "used",
            "images": get_image("OIP (3).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("T-shirt/top"),
            "product_name": "Nike black T-shirt",
            "price": 30000,
            "condition": "used",
            "images": get_image("download (2).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Trouser"),
            "product_name": "Merlin eiger waterproof",
            "price": 120000,
            "condition": "new",
            "images": get_image("download (4).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Trouser"),
            "product_name": "Ootd baggy pants",
            "price": 95000,
            "condition": "new",
            "images": get_image("download (5).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Trouser"),
            "product_name": "Cargo pants",
            "price": 60000,
            "condition": "used",
            "images": get_image("OIP (4).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Trouser"),
            "product_name": "Sirwal jogger pants original",
            "price": 85000,
            "condition": "used",
            "images": get_image("OIP (5).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Trouser"),
            "product_name": "Jogger motif batik",
            "price": 145000,
            "condition": "new",
            "images": get_image("OIP (6).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Trouser"),
            "product_name": "Eiger alpine pants",
            "price": 105000,
            "condition": "new",
            "images": get_image("OIP (7).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Sandal"),
            "product_name": "Swallow",
            "price": 20000,
            "condition": "new",
            "images": get_image("OIP (8).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Sandal"),
            "product_name": "Sandal gunung - Eiger",
            "price": 120000,
            "condition": "new",
            "images": get_image("OIP (9).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Sandal"),
            "product_name": "Black panther",
            "price": 85000,
            "condition": "new",
            "images": get_image("OIP (10).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Sandal"),
            "product_name": "Classic - pakalolo",
            "price": 70000,
            "condition": "used",
            "images": get_image("OIP (11).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Sandal"),
            "product_name": "Sandal kulit",
            "price": 45000,
            "condition": "used",
            "images": get_image("OIP (12).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Bag"),
            "product_name": "Tas sekolah",
            "price": 250000,
            "condition": "new",
            "images": get_image("OIP (16).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Bag"),
            "product_name": "Tas untuk travel",
            "price": 230000,
            "condition": "new",
            "images": get_image("OIP (13).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Bag"),
            "product_name": "Tote bag merah",
            "price": 120000,
            "condition": "new",
            "images": get_image("OIP (14).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Bag"),
            "product_name": "Tas kulit",
            "price": 70000,
            "condition": "used",
            "images": get_image("OIP (15).jpeg"),
            "description": "Lorem ipsum",
        },
        {
            "category": get_category("Bag"),
            "product_name": "Gucci",
            "price": 125000,
            "condition": "used",
            "images": get_image("OIP (17).jpeg"),
            "description": "Lorem ipsum",
        },        
    ]

    run_query(delete(Products), True)

    for val in data:
        image_name = f"{val['product_name']}-{val['category']}-{val['condition']}-{uuid.uuid4()}.jpg"
        uid = uuid.uuid4()

        run_query(
            insert(Images).values(
                id=uid,
                title=image_name,
                image=val["images"],
                create_at=format_datetime(),
                create_by="Developer"
            ), True
        )

        run_query(
            insert(Products).values(
                id=uid,
                category_id=val["category"],
                title=val["product_name"],
                price=val["price"],
                condition=val["condition"],
                image=f"/image/{image_name}",
                product_detail=val["description"],
                create_at=format_datetime(),
                create_by="Developer"
            ), True
        )
        