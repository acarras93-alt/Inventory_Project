from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

import inventory_v4 as app


class DummyRepository:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path


class FakeService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []
        self.behavior: dict[str, Any] = {}

    def _record(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((method_name, args, kwargs))
        action = self.behavior.get(method_name)

        if isinstance(action, BaseException):
            raise action

        if callable(action):
            return action(*args, **kwargs)

        return action

    def add_product(
        self, product_id: int, name: str, price: float, stock_quantity: int
    ) -> Any:
        return self._record(
            "add_product",
            product_id=product_id,
            name=name,
            price=price,
            stock_quantity=stock_quantity,
        )

    def list_products(self) -> Any:
        return self._record("list_products")

    def find_product_by_id(self, product_id: int) -> Any:
        return self._record("find_product_by_id", product_id)

    def rename_product(self, product_id: int, new_name: str) -> Any:
        return self._record("rename_product", product_id, new_name)

    def update_price(self, product_id: int, new_price: float) -> Any:
        return self._record("update_price", product_id, new_price)

    def update_stock(self, product_id: int, new_stock_quantity: int) -> Any:
        return self._record("update_stock", product_id, new_stock_quantity)

    def delete_product(self, product_id: int) -> Any:
        return self._record("delete_product", product_id)


def install_composition(
    monkeypatch: pytest.MonkeyPatch, fake_service: FakeService
) -> None:
    monkeypatch.setattr(app, "JSONproductRepository", DummyRepository)
    monkeypatch.setattr(app, "InventoryService", lambda _repository: fake_service)


def install_inputs(
    monkeypatch: pytest.MonkeyPatch,
    values: list[str],
    prompts: list[str],
) -> None:
    answers: Iterator[str] = iter(values)

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(answers)

    monkeypatch.setattr("builtins.input", fake_input)


def test_invalid_option_shows_message_and_retries(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_service = FakeService()
    install_composition(monkeypatch, fake_service)

    prompts: list[str] = []
    install_inputs(monkeypatch, ["9", "0"], prompts)

    app.main()

    captured = capsys.readouterr()

    assert "Invalid option" in captured.out
    assert prompts.count("Choose an option: ") == 2
    assert "Exiting inventory system." in captured.out


def test_option_0_exits_system(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_service = FakeService()
    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, ["0"], [])

    app.main()

    captured = capsys.readouterr()

    assert "Exiting inventory system." in captured.out
    assert fake_service.calls == []


def test_show_menu_keeps_exact_content_order_punctuation_and_initial_blank_line(
    capsys: pytest.CaptureFixture[str],
) -> None:
    app.show_menu()

    captured = capsys.readouterr()

    assert captured.out == (
        "\n=== INVENTORY SYSTEM V4 ===\n"
        "1. Add product.\n"
        "2. List products.\n"
        "3. Finds product by ID.\n"
        "4. Rename product.\n"
        "5. Update product price.\n"
        "6. Update product stock.\n"
        "7. Delete product.\n"
        "0. Exit.\n"
    )


def test_option_1_collects_values_calls_add_product_and_prints_success(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_service = FakeService()
    install_composition(monkeypatch, fake_service)

    prompts: list[str] = []
    install_inputs(monkeypatch, ["1", "10", "Apples", "2.5", "7", "0"], prompts)

    app.main()
    captured = capsys.readouterr()

    assert (
        "add_product",
        (),
        {
            "product_id": 10,
            "name": "Apples",
            "price": 2.5,
            "stock_quantity": 7,
        },
    ) in fake_service.calls
    assert "Product added successfully." in captured.out
    assert "Exiting inventory system." in captured.out
    assert prompts == [
        "Choose an option: ",
        "Product ID: ",
        "Product name: ",
        "Product price: ",
        "Stock quantitty: ",
        "Choose an option: ",
    ]


def test_option_2_lists_products_and_prints_python_list_repr(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_service = FakeService()
    fake_service.behavior["list_products"] = ["P1", "P2"]
    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, ["2", "0"], [])

    app.main()
    captured = capsys.readouterr()

    assert ("list_products", (), {}) in fake_service.calls
    assert "['P1', 'P2']" in captured.out


@pytest.mark.parametrize(
    ("option", "method_name", "extra_inputs", "expected_args", "expected_message"),
    [
        ("3", "find_product_by_id", ["22"], (22,), "PRODUCT-22"),
        (
            "4",
            "rename_product",
            ["22", "Updated"],
            (22, "Updated"),
            "Stock renamed successfully.",
        ),
        (
            "5",
            "update_price",
            ["22", "9.5"],
            (22, 9.5),
            "Product price updated successfully.",
        ),
        (
            "6",
            "update_stock",
            ["22", "11"],
            (22, 11),
            "Product stock updated successfully.",
        ),
        ("7", "delete_product", ["22"], (22,), "Product deleted successfully."),
    ],
)
def test_options_3_to_7_call_service_and_keep_success_behavior(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    option: str,
    method_name: str,
    extra_inputs: list[str],
    expected_args: tuple[Any, ...],
    expected_message: str,
) -> None:
    fake_service = FakeService()

    if option == "3":
        fake_service.behavior["find_product_by_id"] = "PRODUCT-22"

    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, [option, *extra_inputs, "0"], [])

    app.main()
    captured = capsys.readouterr()

    matching_calls = [call for call in fake_service.calls if call[0] == method_name]
    assert len(matching_calls) == 1
    assert matching_calls[0][1] == expected_args
    assert expected_message in captured.out
    assert "Exiting inventory system." in captured.out


@pytest.mark.parametrize(
    ("option", "extra_inputs", "expected_prompts"),
    [
        (
            "3",
            ["22"],
            ["Choose an option: ", "Product ID: ", "Choose an option: "],
        ),
        (
            "4",
            ["22", "Updated"],
            [
                "Choose an option: ",
                "Product ID: ",
                "New product name: ",
                "Choose an option: ",
            ],
        ),
        (
            "5",
            ["22", "9.5"],
            ["Choose an option: ", "Product ID: ", "New price: ", "Choose an option: "],
        ),
        (
            "6",
            ["22", "11"],
            [
                "Choose an option: ",
                "Product ID: ",
                "New stock quantity: ",
                "Choose an option: ",
            ],
        ),
        (
            "7",
            ["22"],
            ["Choose an option: ", "Product ID: ", "Choose an option: "],
        ),
    ],
)
def test_options_3_to_7_keep_exact_prompt_sequences(
    monkeypatch: pytest.MonkeyPatch,
    option: str,
    extra_inputs: list[str],
    expected_prompts: list[str],
) -> None:
    fake_service = FakeService()

    if option == "3":
        fake_service.behavior["find_product_by_id"] = "PRODUCT-22"

    install_composition(monkeypatch, fake_service)

    prompts: list[str] = []
    install_inputs(monkeypatch, [option, *extra_inputs, "0"], prompts)

    app.main()

    assert prompts == expected_prompts


@pytest.mark.parametrize(
    ("option", "extra_inputs"),
    [
        ("2", []),
        ("3", ["22"]),
        ("4", ["22", "Updated"]),
        ("5", ["22", "9.5"]),
        ("6", ["22", "11"]),
        ("7", ["22"]),
    ],
)
def test_options_2_to_7_repeat_menu_after_operation_then_exit_with_0(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    option: str,
    extra_inputs: list[str],
) -> None:
    fake_service = FakeService()
    fake_service.behavior["list_products"] = ["P1"]

    if option == "3":
        fake_service.behavior["find_product_by_id"] = "PRODUCT-22"

    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, [option, *extra_inputs, "0"], [])

    app.main()
    captured = capsys.readouterr()

    assert captured.out.count("=== INVENTORY SYSTEM V4 ===") == 2
    assert "Exiting inventory system." in captured.out


def test_option_1_input_validation_retries_keep_messages_and_then_succeeds(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_service = FakeService()
    install_composition(monkeypatch, fake_service)

    install_inputs(
        monkeypatch,
        [
            "1",
            "abc",
            "10",
            "   ",
            "Milk",
            "x",
            "-1",
            "3.5",
            "-3",
            "4",
            "0",
        ],
        [],
    )

    app.main()
    captured = capsys.readouterr()

    assert "Invalid number." in captured.out
    assert "The value must be zero or greater." in captured.out
    assert "It cannot be empty" in captured.out
    assert (
        "add_product",
        (),
        {
            "product_id": 10,
            "name": "Milk",
            "price": 3.5,
            "stock_quantity": 4,
        },
    ) in fake_service.calls


def test_option_1_maps_product_already_exists_error_with_print_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_service = FakeService()
    fake_service.behavior["add_product"] = app.ProductAlreadyExistsError("dup")
    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, ["1", "1", "Name", "1", "1", "0"], [])

    app.main()
    captured = capsys.readouterr()

    assert "dup" in captured.out


@pytest.mark.parametrize(
    ("option", "method_name", "extra_inputs"),
    [
        ("3", "find_product_by_id", ["10"]),
        ("4", "rename_product", ["10", "Name"]),
        ("5", "update_price", ["10", "5"]),
        ("6", "update_stock", ["10", "2"]),
        ("7", "delete_product", ["10"]),
    ],
)
def test_product_not_found_uses_print_error_on_supported_options(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    option: str,
    method_name: str,
    extra_inputs: list[str],
) -> None:
    fake_service = FakeService()
    fake_service.behavior[method_name] = app.ProductNotFoundError("missing")
    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, [option, *extra_inputs, "0"], [])

    app.main()
    captured = capsys.readouterr()

    assert "missing" in captured.out


@pytest.mark.parametrize(
    ("option", "method_name", "extra_inputs"),
    [
        ("1", "add_product", ["1", "A", "1", "1"]),
        ("2", "list_products", []),
        ("3", "find_product_by_id", ["1"]),
        ("4", "rename_product", ["1", "A"]),
        ("5", "update_price", ["1", "1"]),
        ("6", "update_stock", ["1", "1"]),
        ("7", "delete_product", ["1"]),
    ],
)
def test_storage_error_prefix_is_preserved(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    option: str,
    method_name: str,
    extra_inputs: list[str],
) -> None:
    fake_service = FakeService()
    fake_service.behavior[method_name] = app.InventoryStorageError("io")
    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, [option, *extra_inputs, "0"], [])

    app.main()
    captured = capsys.readouterr()

    assert "Storage error: io" in captured.out


@pytest.mark.parametrize(
    ("option", "method_name", "extra_inputs"),
    [
        ("1", "add_product", ["1", "A", "1", "1"]),
        ("4", "rename_product", ["1", "A"]),
        ("5", "update_price", ["1", "1"]),
        ("6", "update_stock", ["1", "1"]),
    ],
)
def test_type_and_value_errors_map_to_invalid_product_data(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    option: str,
    method_name: str,
    extra_inputs: list[str],
) -> None:
    for error in (TypeError("bad type"), ValueError("bad value")):
        fake_service = FakeService()
        fake_service.behavior[method_name] = error
        install_composition(monkeypatch, fake_service)
        install_inputs(monkeypatch, [option, *extra_inputs, "0"], [])

        app.main()
        captured = capsys.readouterr()

        assert "Invalid product data:" in captured.out


def test_uncaught_exception_still_propagates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_service = FakeService()
    fake_service.behavior["list_products"] = RuntimeError("boom")
    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, ["2"], [])

    with pytest.raises(RuntimeError, match="boom"):
        app.main()


@pytest.mark.parametrize(
    ("option", "method_name", "extra_inputs"),
    [
        ("2", "list_products", []),
        ("3", "find_product_by_id", ["10"]),
        ("7", "delete_product", ["10"]),
    ],
)
@pytest.mark.parametrize(
    ("error_type", "message"),
    [(TypeError, "bad type"), (ValueError, "bad value")],
)
def test_type_and_value_errors_propagate_in_options_2_3_and_7(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    option: str,
    method_name: str,
    extra_inputs: list[str],
    error_type: type[Exception],
    message: str,
) -> None:
    fake_service = FakeService()
    fake_service.behavior[method_name] = error_type(message)
    install_composition(monkeypatch, fake_service)
    install_inputs(monkeypatch, [option, *extra_inputs], [])

    with pytest.raises(error_type, match=message):
        app.main()

    captured = capsys.readouterr()
    assert "Invalid product data:" not in captured.out
