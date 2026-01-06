import json
from .product_model import Product
import os

# Always resolve products.json relative to the directory containing cli.py
CLI_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cli.py')))
PRODUCTS_FILE = os.path.join(CLI_DIR, 'products.json')

class ProductRepository:
    # Define canonical product fields here for easy modification
    PRODUCT_FIELDS = [
        'id', 'title', 'attributes', 'link', 'datasheet', 'guide', 'image', 'quantity', 'price',
        'power', 'material', 'dimensions', 'certifications', 'specifications', 'location'
    ]

    def __init__(self, file_path=PRODUCTS_FILE):
        self.file_path = file_path

    def load_products(self):
        if not os.path.exists(self.file_path):
            # Create the file as an empty JSON array
            with open(self.file_path, 'w') as f:
                json.dump([], f)
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return [Product(p) for p in data if not (p.get('deleted') is True or p.get('deleted') == 'True')]

    def save_products(self, products):
        # Remove blank fields before saving
        def clean(product_data):
            return {k: v for k, v in product_data.items() if v not in ('', None, [])}
        with open(self.file_path, 'w') as f:
            json.dump([clean(p.data) for p in products], f, indent=2)

    def create_empty_product(self, title):
        from .product_model import Product
        product_data = {field: '' for field in self.PRODUCT_FIELDS}
        product_data['title'] = title
        return Product(product_data)
