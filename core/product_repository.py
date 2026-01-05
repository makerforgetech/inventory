import json
from .product_model import Product
import os

PRODUCTS_FILE = 'products.json'

class ProductRepository:
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
        with open(self.file_path, 'w') as f:
            json.dump([p.data for p in products], f, indent=2)

    def create_empty_product(self, title):
        # Minimal required fields for a new product
        from .product_model import Product
        product_data = {
            'product_id': '',
            'product_title': title,
            'product_attr': '',
            'product_link': '',
            'product_image': '',
            'product_amount': '',
            'product_price': '',
            'Voltage/Power': '',
            'Material': '',
            'Dimensions': '',
            'Certifications': '',
            'Key_Specs': '',
            'location': ''
        }
        return Product(product_data)
