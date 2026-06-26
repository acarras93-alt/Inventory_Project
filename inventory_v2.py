"""
Inventory Management System

Use case:
Manage products in memory through a console menu.

Main entity:
Product

Layers:
- Domain: Product
- Service: InventoryManager
- Interface: console menu
- Orchestration: main()

Main actions:
- Add product
- List products
- Search product
- Update stock
- Delete product

Add product with duplicated ID
Add product with negative price
Add product with negative stock
Search non-existing product
Update non-existing product
Delete non-existing product

1. Validate user input in the interface
2. Validate business rules in the service
3. Add domain-level validation only when the entity must protect itself
"""
# DOMAIN EXCEPTIONS
class ProductAlreadyExistsError(Exception):
    """Raised when trying to add a product with an existing ID."""
    pass

class ProductNotFoundError(Exception):
    """Raised when a product cannot be found in the inventory"""
    pass
    
# DOMAIN MODEL
class Product:
    """Domain entity represent a product in the inventory"""
    
    def __init__(
        self, 
        product_id:int, # Validated at creation and protected afterwards
        name: str, # Can be modified, but validated
        price: float, # Can be modified, but validated
        stock_quantity: int # Can be modified, but validated
    ):
        self._product_id = self._validate_product_id(product_id)
        self._name = self._validate_name(name)
        self._price = self._validate_price(price)
        self._stock_quantity = self._validate_stock_quantity(stock_quantity)
        
    @staticmethod
    def _validate_product_id(product_id: int) -> int:
        if not isinstance(product_id, int):
            raise TypeError("Product ID must be an integer.")

        if product_id < 0:
            raise ValueError("Product ID must be zero or greater.")

        return product_id
    
    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        
        name.strip()
        
        if not name:
            raise ValueError("Name cannot be empty.")
        
        return name
    
    @staticmethod
    def _validate_price(price: float) -> float:
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")
        
        if price < 0:
            raise ValueError("Price must be zero or greater.")
        
        return price
    
    @staticmethod
    def _validate_stock_quantity(stock_quantity: int) -> int:

        if not isinstance(stock_quantity, int):
            raise TypeError("Stock quantity must be an integer.")

        if stock_quantity < 0:
            raise ValueError("Stock quantity must be zero or greater.")

        return stock_quantity
    
    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = self._validate_name(value)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = self._validate_price(value)

    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value: int) -> None:
        self._stock_quantity = self._validate_stock_quantity(value)
        
    def update_stock(self, new_stock_quantity: int) -> None:
        self.stock_quantity = new_stock_quantity
    
    def update_price(self, new_price: float) -> None:
        self.price = new_price
    
    def rename(self, new_name: str) -> None:
        self.name = new_name

    def __str__(self) -> str:
        return (

            f"[{self.product_id}] {self.name} | "
            f"Price: {self.price:.2f} | "
            f"Stock: {self.stock_quantity}"
        )

# SERVICE LAYER
class InventoryManager:
    """Coordinates inventory operations for products."""
    
    def __init__(self):
        self._products_by_id: dict[int, Product] = {}
        
    def add_product(self, product: Product) -> None:
        """Adds a product to the inventory.
        
        Raises:
            ProductAlreadyExistsError: if the product ID already exists.
        """
        if product.product_id in self._products_by_id:
            raise ProductAlreadyExistsError(
                f"Product with ID {product.product_id} already exists"
            )

        self._products_by_id[product.product_id] = product
    
    def list_products(self) -> list[Product]:
        """Returns all products currently stored in the inventory."""
        return list(self._products_by_id.values())
    
    def find_product_by_id(self, product_id: int) -> Product:
        """Finds a product by its ID.
        
        Raises:
            ProductNotFoundError: if the product does not exist.
        """
        product = self._products_by_id.get(product_id)
        
        if product is None:
            raise ProductNotFoundError(
                f"Product with ID {product_id} was not found"
            )
        
        return product 
    
    def update_stock(self, product_id: int, new_stock_quantity: int) -> None:
        """Updates the stock quantity of an existing product."""
        product = self.find_product_by_id(product_id)
        product.update_stock(new_stock_quantity)
    
    def update_price(self, product_id: int, new_price: float) -> None:
        """Update the price of an existing product."""
        product = self.find_product_by_id(product_id)
        product.update_price(new_price)
    
    def delete_product(self, product_id: int) -> None:
        """Removes a product from the inventory."""
        if product_id not in self._products_by_id:
            raise ProductNotFoundError(
                f"Product with ID {product_id} was not found"
            )
        
        del self._products_by_id[product_id]

# INTERFACE
def show_menu() -> None:
        print("\n=== INVENTORY SYSTEM (V2) ===")
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
        str(text)
        
        if text:
            return text
        
        print("It cannot be empty.")
        
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
            try:
                product = ask_product_data() # creates the Product
                manager.add_product(product) # store the Product
            
            except ProductAlreadyExistsError as error:
                print(error)
            
            except(TypeError, ValueError) as error:
                print(f"Invalid product data: {error}")
            
        elif option == "2":
            products = manager.list_products()
            print_products(products)

        elif option == "3":
            product_id = ask_positive_int("Product ID: ")
            
            try:
                product = manager.find_product_by_id(product_id)
                print_product(product)

            except ProductNotFoundError as error:
                print(error)

        elif option == "4":
            product_id = ask_positive_int("Product ID: ")
            new_stock_quantity = ask_positive_int("New stock quantity: ")

            try:
                manager.update_stock(product_id, new_stock_quantity)
                print("Stock updated successfully.")
            except ProductNotFoundError as error:
                print(error)
                
        elif option == "5":
            product_id = ask_positive_int("Product ID: ")
            
            try:
                manager.delete_product(product_id)
                print("Product deleted successfully.")
            except ProductNotFoundError as error:
                print(error)

if __name__ == "__main__":
    main()