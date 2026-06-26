"""Inventory System V4

Objetivo de esta versión:
- El servicio deja de trabajar contra JSON directamente.
- El servicio trabaja contra un repositorio de productos.
- El repositorio es la puerta de acceso a la colección de productos.
- JSON es una una implementación concreta del repositorio.
- Memoria es otra implementación concreta útil para tests.

Arquitectura:

- Domain:
    Product
- Domain exceptions:
    ProductAlreadyExistsError
    ProductNotFoundError
    InventoryStorageError
- Infrastructure exception:
    InventoryStorageError
- Repository contract:
    ProductRepository
- Repository implementations:
    InMemoryProductRepository
    JSONProductRepository
- Service:
    InventoryService
- Interface / Orchestration:
    funciones de consola + main

"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path

# DOMAIN EXCEPTIONS
class ProductAlreadyExistsError(Exception):
    """Raised when trying to add a product with an existing ID."""
    pass

class ProductNotFoundError(Exception):
    """Raised when a product cannot be found in the inventory"""
    pass

class InventoryStorageError(Exception):
    """Raised when inventory persistence operations fail."""
    pass
    
# DOMAIN MODEL
class Product:
    """Domain entity represent a product in the inventory.
    
    Esta clase protege sus propias reglas:
    - product_id debe ser int >= 0
    - name debe ser str no vacio
    - price debe ser int/float >= 0
    - stock_quantity debe ser int >= 0
    """
    
    def __init__(
        self, 
        product_id:int, 
        name: str,
        price: float, 
        stock_quantity: int 
    ) -> None:
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
        
        cleaned_name = name.strip()
        
        if not cleaned_name:
            raise ValueError("Name cannot be empty.")
        
        return cleaned_name
    
    @staticmethod
    def _validate_price(price: float) -> float:
        if not isinstance(price, int) and not isinstance (price, float):
            raise TypeError("Price must be a number.")
        
        if price < 0:
            raise ValueError("Price must be zero or greater.")
        
        return float(price)
    
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
        
    def rename(self, new_name: str) -> None:
        self.name = new_name
    
    def update_price(self, new_price: float) -> None:
        self.price = new_price
    
    def update_stock(self, new_stock_quantity: int) -> None:

        self.stock_quantity = new_stock_quantity
    
    def to_dict(self) -> dict:
        """Convierte la entidad a formato serializable.
        
        En una version más avanzada podemos movert esto a un mapper/DTO,
        pero para mi V4 actual está bien mantenerlo aquí.
        """
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Reconsdtruye una entidad Product con datos cargados.
        
        Importante aunque los datos vengas de JSON, pasan por el constructos,
        por tanto las validaciones de dominio se vuelven a aplicar.
        """
        return cls(
            product_id=data["product_id"],
            name = data["name"],
            price = data["price"],
            stock_quantity = data["stock_quantity"],
        )
        
    def __str__(self) -> str:
        return (
            f"[{self.product_id}] {self.name} | "
            f"Price: {self.price:.2f} | "
            f"Stock: {self.stock_quantity}"
        )

# REPOSITORY CONTRACT
class ProductRepository(ABC):
    """
    Contrato del respositorio de productos.
    
    Esta es la pieza clave de V4.
    
    El servicio no depende de esta abstracción.
    El servicio NO sabe si los datos vienen de:
    - JSON
    - Memoria
    - SQLite
    - PostgreSQL
    - API externa
    
    Regla mental:
    ProductReposiroty = puerta de acceso a la colección de productos.
    """
    @abstractmethod
    def add(self, product: Product) -> None:
        """Add a new product to the colletion."""
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Product:
        """Returns a product by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def list_all(self)-> list[Product]:
        """Returns all products from the collection."""
        raise NotImplementedError
    
    @abstractmethod
    def update(self, porduct: Product)-> None:
        """Updates an existing product."""
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, product_id: int)-> None:
        """"""
        raise NotImplementedError

# IN-MEMORY REPOSITORY
class InMemoryProductRepository(ProductRepository):
    """Repositorio en memoria.
    
    Uso principal:
    - test de servicio
    - pruebas rápidas
    - desarrollo sin tocar archivos
    
    Este repositorio implementa el mismo contrato que JSONProductRepository.
    Por eso InventoryService puede trabajar con ambos.
    """
    def __init__(self) -> None:
        self._products_by_id: dict[int, Product] = {}
        
    def add(self, product: Product) -> None:
        if product.product_id in self._products_by_id:
            raise ProductAlreadyExistsError(
                f"Product with ID {product.product_id} already exists"
            )

        self._products_by_id[product.product_id] = product
    
    def get_by_id(self, product_id: int) -> Product:
        product = self._products_by_id.get(product_id)
        
        if product is None:
            raise ProductNotFoundError(
                f"Product with ID {product_id} was not found."
            )
        return product 
    
    def list_all(self) -> list[Product]:
        products = []
        
        for product in self._products_by_id.values():
            products.append(product)
            
        return products
    
    def update(self, product: Product) -> None:
        if product.product_id not in self._products_by_id:
            raise ProductNotFoundError(
                f"Product with ID {product.product_id} was not found."
            )
        
        self._products_by_id[product.product_id] = product
    
    def delete(self, product_id: int) -> None:
        if product_id not in self._products_by_id:
            raise ProductNotFoundError(
                f"Product with ID {product_id} was not found."
            )
        
        del self._products_by_id[product_id]
        
# JSON REPOSITORY
class JSONproductRepository(ProductRepository):
    """Implementación JSON del repositorio
    
    Esta clase sí conoce JSON.
    Esta clase sí conoce el archivo.
    Esta clase sí sabe cargar y guardar.
    """
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
    
    
    def add(self, product: Product) -> None:
        products = self.list_all()
        
        for exisiting_product in products:
            if exisiting_product.product_id == product.product_id:
                raise ProductAlreadyExistsError(
                    f"Product with ID {product.product_id} already exists."
                )
        
        products.append(product)
        self._save_all(products)
        
    def get_by_id(self, product_id: int) -> Product:
        products = self.list_all()
        
        for product in products:
            if product.product_id == product_id:
                return product
            
        raise ProductNotFoundError(
                f"Product with ID {product_id} was not found."
            )
            
    def list_all(self) -> list[Product]:
        if not self.file_path.exists():
            return []
        
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                products_data = json.load(file)
            
            if not isinstance(products_data, list):
                raise InventoryStorageError(
                    "Invalid JSON structure. Expected a list of products."
                )
            
            products = []

            for product_data in products_data:
                product = Product.from_dict(product_data)
                products.append(product)

            return products
        
        except json.JSONDecodeError as error:
            raise InventoryStorageError(f"Invalid JSON format in {self.file_path.name}: {error}") from error
        
        except OSError as error:
            raise InventoryStorageError("Products could not be loaded.") from error
        
        except KeyError as error:
            raise InventoryStorageError(
                f"Invalid product data. Missing field: {error}."
            ) from error
        
        except TypeError as error:
            raise InventoryStorageError(
                f"Invalid product data type: {error}."
            ) from error
        
        except ValueError as error:
            raise InventoryStorageError(
                f"Invalid product value: {error}."
            ) from error
    
    def update(self, product: Product) -> None:
        products = self.list_all()
        updated_products = []
        product_was_found = False

        for existing_product in products:
            if existing_product.product_id == product.product_id:
                updated_products.append(product)
                product_was_found = True
            else:
                updated_products.append(existing_product)

        if not product_was_found:
            raise ProductNotFoundError(
                f"Product with ID {product.product_id} was not found."
            )

        self._save_all(updated_products)

    def delete(self, product_id: int) -> None:
        products = self.list_all()
        remaining_products = []
        product_was_found = False
        
        for product in products:
            if product.product_id == product_id:
                product_was_found = True

            else:
                remaining_products.append(product)
        if not product_was_found:
            raise ProductNotFoundError(
                f"Product with ID {product_id} was not found."
            )

        self._save_all(remaining_products)
    
    def _save_all(self, products: list[Product]) -> None:
        """Saves a list of Product objects into a JSON file."""
        products_data = []
        
        for product in products:
            products_data.append(product.to_dict())
                
        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(products_data, file, indent=4)
        
        except OSError as error:
            raise InventoryStorageError("Products could not be saved.") from error
        
# SERVICE LAYER
class InventoryService:
    """
    Service Layer / Use Cases
    
    Coordinates busisness operations for product:
    - create product
    - list product
    - find product
    - update price
    - update stock
    - rename product
    - delete product
    
    Punto clave:
    El servicio trabaja contra productRepository.
    No trabaja contra JSON.
    """
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository
        
    def add_product(
        self,
        product_id:int,
        name:str,
        price: float,
        stock_quantity: int,
    ) -> Product:
        product = Product(
            product_id=product_id,
            name=name,
            price=price,
            stock_quantity=stock_quantity
        )
        self._repository.add(product)
        
        return product

    
    def list_products(self) -> list[Product]:
        return self._repository.list_all()
    
    def find_product_by_id(self, product_id: int) -> Product:
        return self._repository.get_by_id(product_id)
    
    def rename_product(self, product_id: int, new_name: str) -> Product:
        product = self._repository.get_by_id(product_id)
        product.rename(new_name)
        self._repository.update(product)
        
        return product
    
    def update_price(self, product_id: int, new_price: float) -> Product:
        product = self._repository.get_by_id(product_id)
        product.update_price(new_price)
        self._repository.update(product)
        
        return product
        
    def update_stock(self, product_id: int, new_stock_quantity: int) ->  Product:
        product = self._repository.get_by_id(product_id)
        product.update_stock(new_stock_quantity)
        self._repository.update(product)
        
        return product
    
    def delete_product(self, product_id: int) -> None:
        product = self._repository.get_by_id(product_id)
        self._repository.delete(product_id)
        

# INTERFACE
def show_menu() -> None:
        print("\n=== INVENTORY SYSTEM V4 ===")
        print("1. Add product.")
        print("2. List products.")
        print("3. Finds product by ID.")
        print("4. Rename product.")
        print("5. Update product price.")
        print("6. Update product stock.")
        print("7. Delete product.")
        print("0. Exit.")

def ask_option() -> str:
    while True:
        option = input("Choose an option: ").strip()
        
        if option in ("0", "1", "2", "3", "4", "5", "6", "7"):
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
            
def print_product(product: Product) -> None:
    print(product)
        
def print_products(products: list[Product]) -> None:
    if not products:
        print("There are no products.")
        return

    for product in products:
        print(product)


# ORCHESTRATION
def main() -> None:
    """Composition root.
    
    Aquí se decide qué implementación concreta usar.
    
    Para consola real:
        JSONPrductRepository
        
    Para tests:
        InMemoryProductRepository
    """
    repository = JSONproductRepository("inventory_data.json")
    service = InventoryService(repository)
    
    while True:
        show_menu()
        option = ask_option()
        
        if option == "0":
            print("Exiting inventory system.")
            break
        
        elif option == "1":
            try:
                product_id = ask_positive_int("Product ID: ")
                name = ask_non_empty_text("Product name: ")
                price = ask_positive_float("Product price: ")
                stock_quantity = ask_positive_int("Stock quantitty: ")
                
                service.add_product(
                    product_id=product_id,
                    name=name,
                    price=price,
                    stock_quantity=stock_quantity
                )
                print("Product added successfully.")

            except ProductAlreadyExistsError as error:
                print(error)
            
            except InventoryStorageError as error:
                print(f"Storage error: {error}")
            
            except(TypeError) as error:
                print(f"Invalid product data: {error}")
            
            except(ValueError) as error:
                print(f"Invalid product data: {error}")
            
        elif option == "2":
            try:
                products = service.list_products()
                print(products)
                
            except InventoryStorageError as error:
                print(f"Storage error: {error}")

        elif option == "3":
            product_id = ask_positive_int("Product ID: ")
            
            try:
                product = service.find_product_by_id(product_id)
                print(product)

            except ProductNotFoundError as error:
                print(error)
            
            except InventoryStorageError as error:
                print(f"Storage error: {error}")

        elif option == "4":
            product_id = ask_positive_int("Product ID: ")
            new_name = ask_non_empty_text("New product name: ")

            try:
                service.rename_product(product_id, new_name)
                print("Stock renamed successfully.")
            
            except ProductNotFoundError as error:
                print(error)
            
            except InventoryStorageError as error:
                print(f"Storage error: {error}")
            
            except(TypeError) as error:
                print(f"Invalid product data: {error}")
            
            except(ValueError) as error:
                print(f"Invalid product data: {error}")
        
        elif option == "5":
            product_id = ask_positive_int("Product ID: ")
            new_price = ask_positive_float("New price: ")
            
            try:
                service.update_price(product_id, new_price)
                print("Product price updated successfully.")
                
            except ProductNotFoundError as error:
                print(error)
            
            except InventoryStorageError as error:
                print(f"Storage error: {error}")
            
            except TypeError as error:
                print(f"Invalid product data: {error}")
            
            except ValueError as error:
                print(f"Invalid product data: {error}")
                
        elif option == "6":
            product_id = ask_positive_int("Product ID: ")
            new_stock_quantity = ask_positive_int("New stock quantity: ")
            
            try:
                service.update_stock(product_id, new_stock_quantity)
                print("Product stock updated successfully.")
            
            except ProductNotFoundError as error:
                print(error)
            
            except InventoryStorageError as error:
                print(f"Storage error: {error}")

            except TypeError as error:
                print(f"Invalid product data: {error}")
            
            except ValueError as error:
                print(f"Invalid product data: {error}")
        
        elif option == "7":
            product_id = ask_positive_int("Product ID: ")
            
            try:
                service.delete_product(product_id)
                print("Product deleted successfully.")
            
            except ProductNotFoundError as error:
                print(error)
    
            except InventoryStorageError as error:
                print(f"Storage error: {error}")

if __name__ == "__main__":
    main()