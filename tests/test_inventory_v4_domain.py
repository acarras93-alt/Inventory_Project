from __future__ import annotations

import pytest

from inventory_v4 import Product


def test_product_accepts_zero_boundaries_and_normalizes_valid_values() -> None:
    product = Product(0, "  Milk  ", 3, 0)

    assert product.product_id == 0
    assert product.name == "Milk"
    assert product.price == 3.0
    assert product.stock_quantity == 0


@pytest.mark.parametrize(
    ("product_id", "name", "price", "stock_quantity"),
    [
        ("1", "Milk", 1, 1),
        (1, 2, 1, 1),
        (1, "Milk", "1", 1),
        (1, "Milk", 1, 1.0),
    ],
)
def test_product_rejects_invalid_field_types(
    product_id: object,
    name: object,
    price: object,
    stock_quantity: object,
) -> None:
    with pytest.raises(TypeError):
        Product(product_id, name, price, stock_quantity)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("product_id", "name", "price", "stock_quantity"),
    [
        (-1, "Milk", 1, 1),
        (1, "", 1, 1),
        (1, "   ", 1, 1),
        (1, "Milk", -0.01, 1),
        (1, "Milk", 1, -1),
    ],
)
def test_product_rejects_invalid_field_values(
    product_id: int,
    name: str,
    price: float,
    stock_quantity: int,
) -> None:
    with pytest.raises(ValueError):
        Product(product_id, name, price, stock_quantity)


def test_product_mutation_helpers_update_only_requested_field() -> None:
    product = Product(1, "Milk", 2.5, 3)

    product.rename("  Oat milk  ")

    assert product.name == "Oat milk"
    assert product.price == 2.5
    assert product.stock_quantity == 3

    product.update_price(4)

    assert product.name == "Oat milk"
    assert product.price == 4.0
    assert product.stock_quantity == 3

    product.update_stock(0)

    assert product.name == "Oat milk"
    assert product.price == 4.0
    assert product.stock_quantity == 0


@pytest.mark.parametrize(
    ("attribute", "invalid_value"),
    [
        ("name", " "),
        ("price", -1),
        ("stock_quantity", -1),
    ],
)
def test_product_invalid_setter_value_preserves_previous_state(
    attribute: str, invalid_value: str | int
) -> None:
    product = Product(1, "Milk", 2.5, 3)

    with pytest.raises(ValueError):
        setattr(product, attribute, invalid_value)

    assert product.name == "Milk"
    assert product.price == 2.5
    assert product.stock_quantity == 3


def test_product_to_dict_exposes_all_current_fields() -> None:
    product = Product(1, "Milk", 2, 3)

    assert product.to_dict() == {
        "product_id": 1,
        "name": "Milk",
        "price": 2.0,
        "stock_quantity": 3,
    }


def test_product_from_dict_reapplies_constructor_normalization() -> None:
    product = Product.from_dict(
        {
            "product_id": 1,
            "name": "  Milk  ",
            "price": 2,
            "stock_quantity": 3,
        }
    )

    assert product.to_dict() == {
        "product_id": 1,
        "name": "Milk",
        "price": 2.0,
        "stock_quantity": 3,
    }


def test_product_from_dict_rejects_invalid_domain_data() -> None:
    with pytest.raises(ValueError):
        Product.from_dict(
            {
                "product_id": 1,
                "name": "Milk",
                "price": -1,
                "stock_quantity": 3,
            }
        )


def test_product_str_uses_current_public_format() -> None:
    product = Product(1, "Milk", 2.5, 3)

    assert str(product) == "[1] Milk | Price: 2.50 | Stock: 3"
