import sys, os, inspect
from core.product_repository import ProductRepository
from core.product_service import ProductService

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_product_details(product, service: ProductService):
    
    updated = False
    def return_to_search(_):
        return 'exit'
    actions = {
        '1': service.add_location,
        '2': service.edit_product_field,
        '3': service.adjust_quantity,
        '4': service.delete_product,
        '0': return_to_search
    }
    # Find the products list in the caller's frame for saving
    def get_products_list():
        for frame in inspect.stack():
            local_vars = frame.frame.f_locals
            if 'products' in local_vars and isinstance(local_vars['products'], list):
                return local_vars['products']
        return None
    products_list = get_products_list()
    repo = ProductRepository()
    while True:
        clear_screen()
        print("Product Details:")
        for key in product.keys():
            print(f"{key.capitalize()}: {product[key]}")
        print()
        print("Options:")
        print("1: Add location")
        print("2: Edit field")
        print("3: Adjust quantity")
        print("4: Delete product")
        print("0: Return to menu")
        choice = input("Enter your choice: ").strip()
        action = actions.get(choice)
        clear_screen()
        if not action:
            print("Invalid choice. Try again.")
            continue
        if action is return_to_search:
            return updated
        result = action(product)
        # Only save if the action returned True or (True, ...) for update
        if (isinstance(result, tuple) and result[0]) or result is True:
            updated = True
            if products_list is not None:
                repo.save_products(products_list)

def search_for_product(products, service: ProductService, repo: ProductRepository):
    results = []
    clear_screen()
    while not results:
        query = input("Enter search term or Enter to exit: ").strip()
        if query == '':
            return
        results = service.search_products(products, query)
        if not results:
            print("No products found.")
    while True:
        clear_screen()
        print("Search Results:")
        for idx, product in enumerate(results, 1):
            print(f"{idx}: {product.get('title', 'Unnamed Product')}")
        sel = input("Enter product number for details (or press Enter to cancel): ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(results):
            idx = int(sel) - 1
            updated = show_product_details(results[idx], service)
            if updated:
                repo.save_products(products)
            break
        else:
            print("Cancelled or invalid selection.")
            input("Press Enter to continue...")
            break

def add_new_product(products, service: ProductService, repo: ProductRepository):
    clear_screen()
    print("Add New Product")
    title = input("Enter product title: ").strip()
    if not title:
        print("Product title cannot be empty.")
        input("Press Enter to return to menu...")
        return
    # Create a new product dict with minimal fields
    new_product = repo.create_empty_product(title)
    products.append(new_product)
    repo.save_products(products)
    show_product_details(new_product, service)

def exit_program(_1, _2, _3):
    print("Exiting.")
    sys.exit(0)
    
def main():
    repo = ProductRepository()
    service = ProductService()
    products = repo.load_products()
    actions = {
        '1': lambda p, s, r: search_for_product(p, s, r),
        '2': add_new_product,
        '3': add_product_with_ai,
        '0': exit_program
    }
    while True:
        clear_screen()
        print("Inventory Management")
        print("1: Search for product")
        print("2: Add new product")
        print("3: Add product with AI")
        print("0: Exit")
        choice = input("Enter your choice: ").strip()
        action = actions.get(choice)
        if action:
            action(products, service, repo)
        else:
            print("Invalid choice. Try again.")
            input("Press Enter to continue...")


def add_product_with_ai(products, service: ProductService, repo: ProductRepository):
    from core.ai_utils import chatgpt_generate
    clear_screen()
    print("Add Product with AI")
    title = input("Enter product name/title/url: ").strip()
    if not title:
        print("Product name cannot be empty.")
        input("Press Enter to return to menu...")
        return

    exclude_fields = ['image', 'datasheet', 'guide']
    fields = [f for f in ProductRepository.PRODUCT_FIELDS if f not in exclude_fields]
    # Prepare prompt for ChatGPT
    prompt = f"""
You are an assistant for inventory management. Given the product name below, generate a JSON object containing the product details with the following fields (do not populate if unknown):\n
{fields}.\n
Do not include links that are not valid or correct\n
If the product name is a URL, attempt to retrieve the webpage and use its content to inform the product details.\n
Product name: {title}\n
Respond ONLY with a valid JSON string. Do NOT include markdown, code blocks, or any extra text. The response must start with '{{' and end with '}}'.
"""
    try:
        ai_response = chatgpt_generate(prompt)
        import json
        # output the AI response for debugging
        print(f"AI Response: {ai_response}")
        product_data = json.loads(ai_response)
        # Ensure product data is flat dictionary of strings only!
        for key in ProductRepository.PRODUCT_FIELDS:
            if key not in product_data:
                product_data[key] = ''
            elif isinstance(product_data[key], dict):
                # Convert dict to comma-separated key:value pairs with readable keys
                def readable_key(k):
                    return k.replace('_', ' ').lower()
                product_data[key] = ', '.join(f"{readable_key(k)}: {v}" for k, v in product_data[key].items())
            elif isinstance(product_data[key], list):
                # Convert list to comma-separated values
                product_data[key] = ', '.join(str(v) for v in product_data[key])
            elif not isinstance(product_data[key], str):
                product_data[key] = str(product_data[key])
        if product_data['quantity'] == '':
            product_data['quantity'] = 1
    except Exception as e:
        print(f"AI failed to generate product: {e}\nResponse was: {ai_response if 'ai_response' in locals() else ''}")
        input("Press Enter to return to menu...")
        return

    # Create Product object and save
    from core.product_model import Product
    new_product = Product(product_data)
    products.append(new_product)
    repo.save_products(products)
    print("Product added with AI!")
    input("Press Enter to view/edit product details...")
    show_product_details(new_product, service)

if __name__ == '__main__':
    main()
