import uuid
import base64
from sqlalchemy import (
    insert,
    delete,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.models.image import Images


def get_image(image_name):
    image_file = open(f"/app/public/images/banners/{image_name}", "rb")
    bs64_str = base64.b64encode(image_file.read())
    return f"base64,{bs64_str.decode('utf-8')}"


def banner_dummy():
    data = [
        {
            "image": get_image("banner4-fashion-sale.png"),
            "title": "banner4-fashion-sale",
        },
        {
            "image": get_image("banner3-fashion-flash.png"),
            "title": "banner3-fashion-flash",
        },
        {
            "image": get_image("banner5-big-sale.png"),
            "title": "banner5-big-sale",
        },
        
        {
            "image": get_image("banner1-shein-deals.png"),
            "title": "banner1-shein-deals",
        },
        {
            "image": get_image("banner2-mid-season-sale.png"),
            "title": "banner2-mid-season-sale",
        },
    ]

    run_query(delete(Images), True)

    for val in data:
        image_name = f"banner-{val['title']}-{uuid.uuid4()}.jpg"
        uid = uuid.uuid4()

        run_query(
            insert(Images).values(
                id=uid,
                title=image_name,
                image=val["image"],
                create_at=format_datetime(),
                create_by="Developer"
            ), True
        )