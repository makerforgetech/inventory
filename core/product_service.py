from .product_model import Product

class ProductService:
    def search_products(self, products, query):
        query = query.lower()
        return [p for p in products if query in p.get('product_title', '').lower() or query in p.get('product_attr', '').lower()]

    def edit_product_field(self, product: Product):
        keys = list(product.keys())
        for fidx, key in enumerate(keys, 1):
            print(f"{fidx}: {key.capitalize()} (current: {product[key]})")
        field_num = input("Enter field number to edit (or press Enter to cancel): ").strip()
        if field_num.isdigit() and 1 <= int(field_num) <= len(keys):
            field = keys[int(field_num)-1]
            current = product[field]
            new_val = input(f"Enter new value for {field} (current: {current}): ").strip()
            product[field] = new_val
            print(f"{field.capitalize()} updated to: {new_val}")
            return True
        else:
            print("Cancelled or invalid selection.")
        return False

    def add_location(self, product: Product):
        loc = input(f"Enter new location (current: {product.get('location', '')}): ").strip()
        if loc:
            product['location'] = loc
            print(f"Location updated to: {loc}")
            return True
        else:
            print("No change made.")
            return False

    def adjust_quantity(self, product: Product):
        current = product.get('product_amount', '')
        new_qty = input(f"Enter new quantity (current: {current}): ").strip()
        if new_qty:
            product['product_amount'] = new_qty
            print(f"Quantity updated to: {new_qty}")
            return True
        else:
            print("No change made.")
            return False

    def delete_product(self, product: Product):
        confirm = input("Are you sure you want to delete this product? (y/N): ").strip().lower()
        if confirm == 'y':
            product.mark_deleted()
            print("Product marked as deleted.")
            return True, True  # updated, exit details
        else:
            print("Delete cancelled.")
            return False, False
