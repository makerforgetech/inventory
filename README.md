# Inventory Management App

<img width="1025" height="676" alt="Screenshot from 2026-02-02 17-14-15" src="https://github.com/user-attachments/assets/624ba0c3-482d-4593-bfb4-44c84d7a0aec" />


## Overview
This is a command-line inventory management application for tracking, searching, and editing product information. It supports manual and AI-assisted product entry, persistent storage in JSON, and flexible product detail management.

This was created to allow a hobbyist electronics enthusiast to keep track of their components and parts inventory without a complicated setup and configuration of a full database system - Simply run the app and start adding/searching your parts!

## Features
- **Search Products:**
  - Search for products by name or attribute.
  - View detailed information for each product.

- **Add New Product (Manual):**
  - Enter product details manually.
  - Edit all fields after creation.

- **Add Product with AI:**
  - Enter a product name/title and let the app use OpenAI's ChatGPT to auto-populate all product fields.
  - Review and edit the generated product details.
  - Note: You will need credit on your OpenAI account to use the AI features.

- **Edit Product Details:**
  - Update any field, including location, quantity, and custom attributes.
  - Delete products (soft delete).

- **Persistent Storage:**
  - All products are stored in `products.json`. Currently this is excluded from version control via `.gitignore`.
  - Example data is provided in `products.json.example`.

## Usage
### Prerequisites
- Python 3.x
- Internet connection (for AI integration)
- An OpenAI API key (for AI product entry)

### Setup
1. **Clone the repository and enter the project directory:**
	```sh
	git clone <repo-url>
	cd inventory
	```

2. **Install dependencies:**
	- The only required external package is `requests`:
	```sh
	pip install requests
	```

3. **Set your OpenAI API key (only required for 'Add product with AI' option):**
	- Obtain an API key from https://platform.openai.com/
	- Set the environment variable before running the app or add it to your shell profile:
	```sh
	export OPENAI_API_KEY=sk-...yourkey...
	```
	Note: You will need credit on your OpenAI account to use the AI features.

### Running the App
You can run the app using the provided script:
```sh
./run.sh
```
Or directly:
```sh
python3 cli.py
```

### Creating an Alias (Optional)
To make it easier to run the app, you can create a shell alias. Add the following line to your shell profile (e.g., `~/.bashrc` or `~/.zshrc`):
```sh
alias inventory='python3 /path/to/inventory/cli.sh'
```
Then, reload your shell profile:
```sh
source ~/.bashrc  # or source ~/.zshrc
```
You can now run the app by simply typing `inventory` in your terminal.

### Main Menu Options
1. **Search for product**
	- Enter a search term to find products. Select a product to view or edit details.
2. **Add new product**
	- Manually enter a new product's title and fill in details.
3. **Add product with AI**
	- Enter a product name/title or URL. The app will use ChatGPT to generate all product fields. You can review and edit the result. Note: some websites like AliExpress may prevent scraping, which can affect the AI's ability to gather information.
0. **Exit**

### Product Details Menu
When viewing a product, you can:
- Add or edit the location
- Edit any field
- Adjust the quantity
- Delete the product (soft delete)
- Return to the main menu

## File Structure
- `cli.py` — Main CLI application
- `core/` — Core logic (models, repository, service, AI integration)
- `products.json` — Main product data file used to store inventory (not in version control, will be created on first run if it doesn't exist)
- `products.json.example` — Example product data
- `run.sh` — Run script

## OpenAI Integration
The "Add product with AI" feature uses the OpenAI ChatGPT API to generate product details from a product name/title or URL. To enable this feature:
1. Set the `OPENAI_API_KEY` environment variable as described above.
2. Ensure you have an internet connection.
3. The app will prompt you for a product name and auto-fill all fields using the API.

## Troubleshooting
- If you see errors related to the OpenAI API, ensure your API key is set and valid.
- If the AI-generated product is not valid JSON, try again or edit the fields manually.

## License
See `LICENSE` for details.
