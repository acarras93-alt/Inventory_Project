"""
Inventory Management System - Version 3

Main goal:
Add JSON persistence to the inventory system while keeping a clean backend-style architecture.

Layers:
- Domain: Product
- Domain exceptions: ProductAlreadyExistsError, ProductNotFoundError
- Service: InventoryManager
- Persistence: JSONInventoryStorage
- Interface: console input/output functions
- Orchestration: main()

V3 improvements:
- Products can be converted to dictionaries using Product.to_dict().
- Products can be restored from dictionaries using Product.from_dict().
- Inventory data is loaded from a JSON file when the program starts.
- Inventory data is saved to a JSON file after add, update and delete operations.
- InventoryManager keeps using dict[int, Product] internally.
- JSON persistence uses list[dict] only for serialization.

Validation strategy:
1. The interface validates user input before creating or updating products.
2. The Product entity validates its own fields to protect object consistency.
3. The service layer validates business rules such as duplicated IDs or missing products.
4. The persistence layer converts between Product objects and JSON-compatible dictionaries.

Manual test cases:
- Start the program with no JSON file.
- Add a valid product.
- Add a product with a duplicated ID.
- Add a product with a negative price.
- Add a product with a negative stock quantity.
- Search for an existing product.
- Search for a non-existing product.
- Update stock for an existing product.
- Update stock for a non-existing product.
- Delete an existing product.
- Delete a non-existing product.
- Exit the program and verify that inventory_data.json is created.
- Run the program again and verify that saved products are loaded correctly.
"""

import json
from pathlib import Path


# DOMAIN EXCEPTIONS
class ProductAlreadyExistsError(Exception):
    """Raised when trying to add a product with an existing ID."""


class ProductNotFoundError(Exception):
    """Raised when a product cannot be found in the inventory"""


class InventoryStorageError(Exception):
    """Raised when inventory persistence operations fail."""


# DOMAIN MODEL
class Product:
    """Domain entity represent a product in the inventory"""

    def __init__(
        self,
        product_id: int,  # Validated at creation and protected afterwards
        name: str,  # Can be modified, but validated
        price: float,  # Can be modified, but validated
        stock_quantity: int,  # Can be modified, but validated
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

        name = name.strip()

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

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            price=data["price"],
            stock_quantity=data["stock_quantity"],
        )

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

    def load_products(self, products: list[Product]) -> None:
        """Loads multiple products into inventory"""
        for product in products:
            self.add_product(product)

    def find_product_by_id(self, product_id: int) -> Product:
        """Finds a product by its ID.

        Raises:
            ProductNotFoundError: if the product does not exist.
        """
        product = self._products_by_id.get(product_id)

        if product is None:
            raise ProductNotFoundError(f"Product with ID {product_id} was not found")
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
        if product_id in self._products_by_id:
            raise ProductNotFoundError(f"Product with ID {product_id} was not found")
        del self._products_by_id[product_id]


# PERSISTENCE LAYER
class JSONInventoryStorage:
    """Handles inventory persistence using a JSON file."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def save_products(self, products: list[Product]) -> None:
        """Saves a list of Product objects into a JSON file."""
        products_data = []

        for product in products:
            products_data.append(product.to_dict())

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(products_data, file, indent=4)

    def load_products(self) -> list[Product]:
        """Loads products from a JSON file.

        If the file does not exist, returns an empty list.

        Raises:
            InventoryStorageError: if the file cannot be read or contains invalid data.
        """
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                products_data = json.load(file)

            products = []

            for product_data in products_data:
                product = Product.from_dict(product_data)
                products.append(product)

            return products

        except json.JSONDecodeError as e:
            raise InventoryStorageError(
                f"Invalid JSON format in {self.file_path.name}: {e}"
            )
        except (KeyError, TypeError, ValueError) as e:
            raise InventoryStorageError(f"Invalid product data structure: {e}")


# INTERFACE
def show_menu() -> None:
    print("\n=== INVENTORY SYSTEM (V3 - JSON) ===")
    print("1. Add product.")
    print("2. List products.")
    print("3. Finds product by ID.")
    print("4. Update product stock.")
    print("5. Update product price.")
    print("6. Delete product.")
    print("0. Exit.")


def ask_option() -> str:
    while True:
        option = input("Choose an option: ").strip()

        if option in ("0", "1", "2", "3", "4", "5", "6"):
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
        product_id=product_id, name=name, price=price, stock_quantity=stock_quantity
    )


def print_product(product: Product) -> None:
    print(product)


def print_products(products: list[Product]) -> None:
    if not products:
        print("There are no products.")
        return

    for product in products:
        print(product)


# ORCHESTRATION
def main():
    manager = InventoryManager()
    storage = JSONInventoryStorage("inventory_data.json")

    try:
        products = storage.load_products()
        manager.load_products(products)
        print("Inventory data loaded successfully.")

    except InventoryStorageError as error:
        print(f"Could not load inventory data: {error}")

    while True:
        show_menu()
        option = ask_option()

        if option == "0":
            storage.save_products(manager.list_products())
            print("Inventory data saved successfully.")
            print("Exiting inventory system.")
            break

        elif option == "1":
            try:
                product = ask_product_data()  # creates the Product
                manager.add_product(product)  # store the Product
                storage.save_products(manager.list_products())
                print("Product added successfully.")

            except ProductAlreadyExistsError as error:
                print(error)

            except (TypeError, ValueError) as error:
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
                storage.save_products(manager.list_products())
                print("Stock updated successfully.")

            except ProductNotFoundError as error:
                print(error)

        elif option == "5":
            product_id = ask_positive_int("Product ID: ")
            new_price = ask_positive_float("New price: ")

            try:
                manager.update_price(product_id, new_price)
                storage.save_products(manager.list_products())
                print("Price updated successfully.")

            except ProductNotFoundError as error:
                print(error)

        elif option == "6":
            product_id = ask_positive_int("Product ID: ")

            try:
                manager.delete_product(product_id)
                storage.save_products(manager.list_products())
                print("Product deleted successfully.")

            except ProductNotFoundError as error:
                print(error)


if __name__ == "__main__":
    main()
