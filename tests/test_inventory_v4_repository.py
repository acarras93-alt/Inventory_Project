from __future__ import annotations

import pytest

from inventory_v4 import (
    InMemoryProductRepository,
    Product,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductRepository,
)


@pytest.fixture
def repository() -> InMemoryProductRepository:
    return InMemoryProductRepository()


def test_product_repository_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        ProductRepository()


def test_in_memory_repository_is_a_product_repository(
    repository: InMemoryProductRepository,
) -> None:
    assert isinstance(repository, ProductRepository)


def test_in_memory_repository_starts_empty(
    repository: InMemoryProductRepository,
) -> None:
    assert repository.list_all() == []


def test_in_memory_repository_adds_and_gets_product_by_id(
    repository: InMemoryProductRepository,
) -> None:
    product = Product(1, "Milk", 2.5, 3)

    assert repository.add(product) is None
    assert repository.get_by_id(1).to_dict() == product.to_dict()


def test_in_memory_repository_lists_all_added_products(
    repository: InMemoryProductRepository,
) -> None:
    repository.add(Product(1, "Milk", 2.5, 3))
    repository.add(Product(2, "Bread", 1.5, 4))

    assert {product.product_id for product in repository.list_all()} == {1, 2}


def test_in_memory_repository_updates_existing_product(
    repository: InMemoryProductRepository,
) -> None:
    repository.add(Product(1, "Milk", 2.5, 3))
    updated_product = Product(1, "Oat milk", 4, 0)

    assert repository.update(updated_product) is None
    assert repository.get_by_id(1).to_dict() == updated_product.to_dict()


def test_in_memory_repository_deletes_existing_product(
    repository: InMemoryProductRepository,
) -> None:
    repository.add(Product(1, "Milk", 2.5, 3))

    assert repository.delete(1) is None
    with pytest.raises(ProductNotFoundError):
        repository.get_by_id(1)


def test_in_memory_repository_rejects_duplicate_id_without_replacing_product(
    repository: InMemoryProductRepository,
) -> None:
    original_product = Product(1, "Milk", 2.5, 3)
    repository.add(original_product)

    with pytest.raises(ProductAlreadyExistsError):
        repository.add(Product(1, "Oat milk", 4, 0))

    assert len(repository.list_all()) == 1
    assert repository.get_by_id(1).to_dict() == original_product.to_dict()


def test_in_memory_repository_missing_get_preserves_collection(
    repository: InMemoryProductRepository,
) -> None:
    product = Product(1, "Milk", 2.5, 3)
    repository.add(product)

    with pytest.raises(ProductNotFoundError):
        repository.get_by_id(2)

    assert [item.to_dict() for item in repository.list_all()] == [product.to_dict()]


def test_in_memory_repository_missing_update_preserves_collection(
    repository: InMemoryProductRepository,
) -> None:
    product = Product(1, "Milk", 2.5, 3)
    repository.add(product)

    with pytest.raises(ProductNotFoundError):
        repository.update(Product(2, "Oat milk", 4, 0))

    assert [item.to_dict() for item in repository.list_all()] == [product.to_dict()]


def test_in_memory_repository_missing_delete_preserves_collection(
    repository: InMemoryProductRepository,
) -> None:
    product = Product(1, "Milk", 2.5, 3)
    repository.add(product)

    with pytest.raises(ProductNotFoundError):
        repository.delete(2)

    assert [item.to_dict() for item in repository.list_all()] == [product.to_dict()]


def test_in_memory_repository_accepts_product_with_zero_values(
    repository: InMemoryProductRepository,
) -> None:
    product = Product(0, "A", 0, 0)

    repository.add(product)

    assert repository.get_by_id(0).to_dict() == product.to_dict()
