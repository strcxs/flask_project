import uuid
import base64
from PIL import Image
from io import BytesIO
from flask import send_file
from sqlalchemy import select
from app.utils.query import run_query
from app.models.image import Images
from . import universal_bp


@universal_bp.route("/<name>", methods=["GET"])
def get_image(name):
    image = run_query(select(Images.image).where(Images.title==name))[0]["image"]
    image = image.split(",")[1]
    title = uuid.uuid4()

    Image.open(BytesIO(base64.b64decode(image))).save(f"{title}.jpg")
    return send_file(f"{title}.jpg", mimetype="image/png")