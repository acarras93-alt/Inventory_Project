from __future__ import annotations

import pytest

from inventory_v4 import (
    InMemoryProductRepository,
    InventoryService,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)


@pytest.fixture
def repository() -> InMemoryProductRepository:
    return InMemoryProductRepository()


@pytest.fixture
def service(repository: InMemoryProductRepository) -> InventoryService:
    return InventoryService(repository)


def test_inventory_service_starts_with_empty_product_list(
    service: InventoryService,
) -> None:
    assert service.list_products() == []


def test_inventory_service_adds_product_and_returns_validated_product(
    service: InventoryService,
) -> None:
    product = service.add_product(1, "  Milk  ", 2, 3)

    assert product.to_dict() == {
        "product_id": 1,
        "name": "Milk",
        "price": 2.0,
        "stock_quantity": 3,
    }
    assert service.find_product_by_id(1).to_dict() == product.to_dict()


def test_inventory_service_lists_added_products_without_order_requirement(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)
    service.add_product(2, "Bread", 1.5, 4)

    assert {product.product_id for product in service.list_products()} == {1, 2}


def test_inventory_service_finds_existing_product(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    assert service.find_product_by_id(1).to_dict() == {
        "product_id": 1,
        "name": "Milk",
        "price": 2.5,
        "stock_quantity": 3,
    }


def test_inventory_service_renames_product_and_preserves_other_fields(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    renamed_product = service.rename_product(1, "  Oat milk  ")

    assert renamed_product.to_dict() == {
        "product_id": 1,
        "name": "Oat milk",
        "price": 2.5,
        "stock_quantity": 3,
    }


def test_inventory_service_updates_price_to_zero_and_preserves_other_fields(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    updated_product = service.update_price(1, 0)

    assert updated_product.to_dict() == {
        "product_id": 1,
        "name": "Milk",
        "price": 0.0,
        "stock_quantity": 3,
    }


def test_inventory_service_updates_stock_to_zero_and_preserves_other_fields(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    updated_product = service.update_stock(1, 0)

    assert updated_product.to_dict() == {
        "product_id": 1,
        "name": "Milk",
        "price": 2.5,
        "stock_quantity": 0,
    }


def test_inventory_service_adds_product_with_zero_values(
    service: InventoryService,
) -> None:
    product = service.add_product(0, "A", 0, 0)

    assert product.to_dict() == {
        "product_id": 0,
        "name": "A",
        "price": 0.0,
        "stock_quantity": 0,
    }


def test_inventory_service_deletes_existing_product(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    assert service.delete_product(1) is None
    with pytest.raises(ProductNotFoundError):
        service.find_product_by_id(1)


def test_inventory_service_rejects_duplicate_id_without_replacing_product(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    with pytest.raises(ProductAlreadyExistsError):
        service.add_product(1, "Oat milk", 4, 0)

    assert [product.to_dict() for product in service.list_products()] == [
        {
            "product_id": 1,
            "name": "Milk",
            "price": 2.5,
            "stock_quantity": 3,
        }
    ]


def test_inventory_service_rejects_invalid_add_without_partial_product(
    service: InventoryService,
) -> None:
    with pytest.raises(ValueError):
        service.add_product(1, "Milk", -1, 3)

    assert service.list_products() == []


def test_inventory_service_missing_find_preserves_collection(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    with pytest.raises(ProductNotFoundError):
        service.find_product_by_id(2)

    assert {product.product_id for product in service.list_products()} == {1}


@pytest.mark.parametrize("operation", ["rename", "price", "stock"])
def test_inventory_service_missing_mutation_preserves_collection(
    service: InventoryService, operation: str
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    with pytest.raises(ProductNotFoundError):
        if operation == "rename":
            service.rename_product(2, "Oat milk")
        elif operation == "price":
            service.update_price(2, 4)
        else:
            service.update_stock(2, 4)

    assert [product.to_dict() for product in service.list_products()] == [
        {
            "product_id": 1,
            "name": "Milk",
            "price": 2.5,
            "stock_quantity": 3,
        }
    ]


def test_inventory_service_missing_delete_preserves_collection(
    service: InventoryService,
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    with pytest.raises(ProductNotFoundError):
        service.delete_product(2)

    assert {product.product_id for product in service.list_products()} == {1}


@pytest.mark.parametrize("operation", ["rename", "price", "stock"])
def test_inventory_service_invalid_mutation_preserves_product_state(
    service: InventoryService, operation: str
) -> None:
    service.add_product(1, "Milk", 2.5, 3)

    with pytest.raises(ValueError):
        if operation == "rename":
            service.rename_product(1, " ")
        elif operation == "price":
            service.update_price(1, -1)
        else:
            service.update_stock(1, -1)

    assert service.find_product_by_id(1).to_dict() == {
        "product_id": 1,
        "name": "Milk",
        "price": 2.5,
        "stock_quantity": 3,
    }
