from loguru import logger

from src.utils import load_json_data
from src.meili import Meili
from src.meili.model import ProductDoc
from src.utils.data_loader import Product


def seed_meili(meili: Meili, length=None):
    logger.info(
        f"seeding {length if length is not None else ''} docs to meili database..."
    )
    products: list[Product] = load_json_data()
    if length is not None:
        products = products[:length]
    meili.add_documents(
        [
            ProductDoc(
                id=str(p.id),
                title=p.name if p.name is not None else "",
                category_name=p.category_name if p.category_name is not None else "",
                current_price=p.current_price if p.current_price is not None else 0,
                image_url=p.images[0],
            )
            for p in products
        ]
    )
    logger.info("seeding meili done.")
