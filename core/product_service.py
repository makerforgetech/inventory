from .product_model import Product

class ProductService:
    def search_products(self, products, query):
        query = query.lower()
        return [p for p in products if query in p.get('title', '').lower() or query in p.get('attributes', '').lower() or query in p.get('seo', '').lower()]

    def edit_product_field(self, product: Product):
        # Import ProductRepository here to avoid circular import
        from .product_repository import ProductRepository
        fields = ProductRepository.PRODUCT_FIELDS
        for fidx, key in enumerate(fields, 1):
            print(f"{fidx}: {key.capitalize()} (current: {product.get(key, '')})")
        field_num = input("Enter field number to edit (or press Enter to cancel): ").strip()
        if field_num.isdigit() and 1 <= int(field_num) <= len(fields):
            field = fields[int(field_num)-1]
            current = product.get(field, '')
            new_val = input(f"Enter new value for {field} (current: {current}): ").strip()
            product[field] = new_val
            print(f"{field.capitalize()} updated to: {new_val}")
            return True
        else:
            print("Cancelled or invalid selection.")
        return False

    def add_location(self, product: Product):
        loc = input(f"Enter new location (current: {product.get('location', '')}): ").strip()
        product['location'] = loc
        print(f"Location updated to: {loc}")
        return True

    def adjust_quantity(self, product: Product):
        current = product.get('quantity', '')
        new_qty = input(f"Enter new quantity (current: {current}): ").strip()
        product['quantity'] = new_qty
        print(f"Quantity updated to: {new_qty}")
        return True

    def delete_product(self, product: Product):
        confirm = input("Are you sure you want to delete this product? (y/N): ").strip().lower()
        if confirm == 'y':
            product.mark_deleted()
            print("Product marked as deleted.")
            return True, True  # updated, exit details
        else:
            print("Delete cancelled.")
            return False, False
