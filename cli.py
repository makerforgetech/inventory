import sys
from core.product_repository import ProductRepository
from core.product_service import ProductService

def clear_screen():
    import os
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
        if action is service.delete_product:
            changed, should_exit = action(product)
            if changed:
                updated = True
            if should_exit:
                return updated
        else:
            if action(product):
                updated = True

def search_for_product(products, service: ProductService, repo: ProductRepository):
    clear_screen()
    query = input("Enter search term: ").strip()
    results = service.search_products(products, query)
    if not results:
        print("No products found.")
        input("Press Enter to continue...")
        return
    while True:
        clear_screen()
        print("Search Results:")
        for idx, product in enumerate(results, 1):
            print(f"{idx}: {product.get('product_title', 'Unnamed Product')}")
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
    title = input("Enter product name/title: ").strip()
    if not title:
        print("Product name cannot be empty.")
        input("Press Enter to return to menu...")
        return

    # Prepare prompt for ChatGPT
    prompt = f"""
You are an assistant for inventory management. Given the product name below, generate a JSON object containing the product details with the following fields (use empty string if unknown):\n
product_id, product_title, product_attr, product_link, product_image, Voltage/Power, Material, Dimensions, Certifications, Key_Specs.\n
Include a link to a datasheet in product_link if possible.\n
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
        # Ensure product_title is set to the user input
        # product_data['product_title'] = title
        product_data['product_amount'] = 1
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
