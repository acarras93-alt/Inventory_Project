"""
Inventory Management System

Use case:
Manage products in memory through a console menu.

Main entity:
Product

Main actions:
- Add product
- List products
- Search product
- Update stock
- Delete product

Layers:
- Domain: Product
- Service: InventoryManager
- Interface: console menu
- Orchestration: main()
"""
from dataclasses import dataclass
from os import name


# DOMAIN MODEL
@dataclass
class Product:
    product_id: int
    name: str
    price: float
    stock_quantity: int

# SERVICE LAYER
class InventoryManager:
    """Coordinates inventory operations for products.
    key   = product ID
    value = Product object
    """
    
    def __init__(self):
        self.products_by_id:  dict[int, Product] = {}
        
    def add_product(self, product: Product):
        """Adds a product to he inventory."""
        self.products_by_id[product.product_id] = product
    
    def list_products(self):
        """Returns all products currently stored in the inventory."""
        return list(self.products_by_id.values())
    
    def find_product_by_id(self, product_id: int):
        """Finds a product by its ID."""
        return self.products_by_id.get(product_id)
    
    def update_stock(self, product_id: int, new_stock_quantity: int):
        """Updates the stock quantity of an existing product."""
        product = self.find_product_by_id(product_id)

        if product is None:
            return False
        
        product.stock_quantity = new_stock_quantity
        return True
    
    def delete_product(self, product_id: int):
        """Removes a product from the inventory."""
        if product_id not in self.products_by_id:
            return False
        
        del self.products_by_id[product_id]
        return True

# INTERFACE
def show_menu() -> None:
        print("\n=== INVENTORY SYSTEM (V1) ===")
        print("1. Add product")
        print("2. List products")
        print("3. Finds product by ID")
        print("4. Update product stock")
        print("5. Delete product")
        print("0. Exit")

def ask_option() -> str:
    while True:
        option = input("Choose an option: ").strip()
        
        if option in ("0", "1", "2", "3", "4", "5"):
            return option
        
        print("Invalid option")

def ask_non_empty_text(message: str) -> str:
    while True:
        text = input(message).strip()
        
        if text:
            return text
        
        print("It cannot be empty")
        
def ask_positive_int(message: str) -> int:

    while True:
        try:
            value = int(input(message).strip())

            if value >= 0:
                return value

            print("The value must be zero or greater.")

        except ValueError:
            print("Invalid number.")

def ask_positive_float(message: str) -> float:
    while True:
        try:
            value = float(input(message).strip())

            if value >= 0:
                return value

            print("The value must be zero or greater.")

        except ValueError:
            print("Invalid number.")
            
def ask_product_data() -> Product:
    product_id = ask_positive_int("Product ID:")
    name = ask_non_empty_text("Product name: ")
    price = ask_positive_float("Product price: ")
    stock_quantity = ask_positive_int("Stock quantity: ")
    
    return Product(
        product_id=product_id,
        name=name,
        price=price,
        stock_quantity=stock_quantity
    )
def print_product(product: Product) -> None:
    print(
        f"[{product.product_id}] {product.name} | "
        f"Price: {product.price:.2f} | "
        f"Stock: {product.stock_quantity}"
    )
        
def print_products(products: list[Product]) -> None:
    if not products:
        print("There are no products.")
        return

    for product in products:
        print(
            f"[{product.product_id}] {product.name} | "
            f"Price: {product.price:.2f} | "
            f"Stock: {product.stock_quantity}"
        )


# ORCHESTRATION
def main():
    manager = InventoryManager()
    
    while True:
        show_menu()
        option = ask_option()
        
        if option == "0":
            print("Exiting inventory system.")
            break
        
        elif option == "1":
            product = ask_product_data() # creates the Product
            manager.add_product(product) # store the Product
            print("Product added successfully")
            
        elif option == "2":
            products = manager.list_products()
            print_products(products)

        elif option == "3":
            product_id = ask_positive_int("Product ID: ")
            product = manager.find_product_by_id(product_id)

            if product is None:
                print("Product not found.")
            else:
                print_product(product)

        elif option == "4":
            product_id = ask_positive_int("Product ID: ")
            new_stock_quantity = ask_positive_int("New stock quantity: ")

            updated = manager.update_stock(product_id, new_stock_quantity)
            
            if updated:
                print("Stock update sucessfully.")
            else:
                print("Product not found.")
                
        elif option == "5":
            product_id = ask_positive_int("Product ID: ")
            
            deleted = manager.delete_product(product_id)
            
            if deleted:
                print("Product deleted sucessfully.")
            else:
                print("Product not found.")

if __name__ == "__main__":
    main()