import json
from loguru import logger
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

from src.clip import CLIP
from src.utils.data_loader import Product
from src.vdb import VDBClient
from src.vdb.models import ProductEmbed, ProductMetadata
from src.utils import load_json_data


def get_image(image_URL):
    response = requests.get(image_URL)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image


def seed_vdb(vdb: VDBClient, length=None):
    logger.info(f"seeding {length if length is not None else ''} vector database...")
    products: list[Product] = load_json_data()
    if length is not None:
        products = products[:length]
    c = CLIP()
    product_embeds = []
    for product in tqdm(products):
        try:
            # TODO: each product has multiple images what we'll gonna do with them?
            # for now just using one image for each product
            img = get_image(product.images[0])
            img_emb = c.image_embedding(img)
            product_emb = ProductEmbed(
                id=str(product.id),
                values=img_emb,
                metadata=ProductMetadata(
                    name=product.name if product.name is not None else "",
                    category_name=product.category_name
                    if product.category_name is not None
                    else "",
                    current_price=product.current_price
                    if product.current_price is not None
                    else 0,
                    image_url=product.images[0],
                ),
            )
            product_embeds.append(product_emb.model_dump())
        except Exception as e:
            logger.exception(e)
            continue

    vdb.batch_upsert(product_embeds)
    logger.info("seeding vdb done.")


if __name__ == "__main__":
    seed_vdb()
