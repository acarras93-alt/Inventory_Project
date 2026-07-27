from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

import inventory_csv_filter as csv_filter


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="")


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_is_strictly_greater_handles_less_equal_and_greater() -> None:
    threshold = Decimal("10")

    assert not csv_filter.is_strictly_greater(Decimal("9.99"), threshold)
    assert not csv_filter.is_strictly_greater(Decimal("10"), threshold)
    assert csv_filter.is_strictly_greater(Decimal("10.01"), threshold)


@pytest.mark.parametrize("raw_value", ["", "abc", "NaN", "Infinity", "-Infinity"])
def test_threshold_invalid_values_return_exit_code_2(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    raw_value: str,
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,1.0\n")

    args = [
        str(input_file),
        str(output_file),
        "--column",
        "price",
    ]

    if raw_value.startswith("-"):
        args.append(f"--threshold={raw_value}")
    else:
        args.extend(["--threshold", raw_value])

    code = csv_filter.main(args)

    captured = capsys.readouterr()

    assert code == 2
    assert captured.err


def test_filter_preserves_columns_order_rows_and_field_strings(tmp_path: Path) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(
        input_file,
        "id,price,name\n1,001.50,A\n2,2.00,B\n3,10.00,C\n",
    )

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "0.40",
        ]
    )

    assert code == 0
    assert read_file(output_file) == "id,price,name\n1,001.50,A\n2,2.00,B\n3,10.00,C\n"


def test_cli_excludes_rows_equal_to_threshold_in_mixed_batch(
    tmp_path: Path,
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(
        input_file,
        "id,price,name\n1,0.50,A\n2,1.00,B\n3,2.00,C\n",
    )

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1.00",
        ]
    )

    assert code == 0
    assert read_file(output_file) == "id,price,name\n3,2.00,C\n"


def test_no_matches_keeps_header_only(tmp_path: Path) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,1\n2,2\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "100",
        ]
    )

    assert code == 0
    assert read_file(output_file) == "id,price\n"


def test_header_only_file_is_valid(tmp_path: Path) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )

    assert code == 0
    assert read_file(output_file) == "id,price\n"


def test_zero_bytes_file_is_invalid_csv_data(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    input_file.write_bytes(b"")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "empty" in captured.err.lower()
    assert not output_file.exists()


def test_missing_column_invalidates_operation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,3\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "stock",
            "--threshold",
            "1",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "column" in captured.err.lower()
    assert not output_file.exists()


@pytest.mark.parametrize(
    "csv_content, expected_error_fragment",
    [
        ("id,price\n1,\n", "must not be empty"),
        ("id,price\n1,abc\n", "valid decimal"),
        ("id,price\n1,NaN\n", "must be finite"),
        ("id,price\n1,Infinity\n", "must be finite"),
        ("id,price\n\n", "row"),
        ("id,price\n1\n", "expected"),
    ],
)
def test_invalid_cell_or_row_invalidates_whole_operation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    csv_content: str,
    expected_error_fragment: str,
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, csv_content)

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert expected_error_fragment in captured.err.lower()
    assert not output_file.exists()


def test_empty_or_duplicate_header_is_invalid(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_empty_header = tmp_path / "input_empty_header.csv"
    output_empty_header = tmp_path / "out_empty_header.csv"
    write_file(input_empty_header, "id,,price\n1,a,2\n")

    duplicate_header_input = tmp_path / "input_duplicate.csv"
    duplicate_header_output = tmp_path / "out_duplicate.csv"
    write_file(duplicate_header_input, "id,price,price\n1,1,2\n")

    code_empty = csv_filter.main(
        [
            str(input_empty_header),
            str(output_empty_header),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )
    captured_empty = capsys.readouterr()

    code_duplicate = csv_filter.main(
        [
            str(duplicate_header_input),
            str(duplicate_header_output),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )
    captured_duplicate = capsys.readouterr()

    assert code_empty == 2
    assert "header" in captured_empty.err.lower()
    assert code_duplicate == 2
    assert "duplicate" in captured_duplicate.err.lower()


def test_input_file_missing_returns_code_1(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "missing.csv"
    output_file = tmp_path / "output.csv"

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
        ]
    )

    captured = capsys.readouterr()

    assert code == 1
    assert "not found" in captured.err.lower()


def test_invalid_output_directory_returns_code_1(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "missing_dir" / "output.csv"
    write_file(input_file, "id,price\n1,1\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )

    captured = capsys.readouterr()

    assert code == 1
    assert "directory" in captured.err.lower() or "write" in captured.err.lower()


def test_output_path_that_is_directory_returns_code_1(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_dir = tmp_path / "existing_output_dir"
    output_dir.mkdir()
    write_file(input_file, "id,price\n1,1\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_dir),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )

    captured = capsys.readouterr()

    assert code == 1
    assert "directory" in captured.err.lower()


def test_input_and_output_same_file_returns_code_2(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    csv_path = tmp_path / "data.csv"
    write_file(csv_path, "id,price\n1,2\n")

    code = csv_filter.main(
        [
            str(csv_path),
            str(csv_path),
            "--column",
            "price",
            "--threshold",
            "1",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "different" in captured.err.lower()


def test_existing_output_without_overwrite_returns_code_2_and_keeps_old_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,2\n")
    write_file(output_file, "legacy\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "overwrite" in captured.err.lower()
    assert read_file(output_file) == "legacy\n"


def test_existing_output_with_overwrite_replaces_file(tmp_path: Path) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,5\n")
    write_file(output_file, "legacy\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
            "--overwrite",
        ]
    )

    assert code == 0
    assert read_file(output_file) == "id,price\n1,5\n"


def test_previous_output_is_protected_when_validation_fails(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,2\n2,abc\n")
    write_file(output_file, "legacy\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
            "--overwrite",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "valid decimal" in captured.err.lower()
    assert read_file(output_file) == "legacy\n"


def test_temp_file_is_cleaned_if_replace_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,2\n")
    write_file(output_file, "legacy\n")

    real_replace = csv_filter.os.replace

    def fake_replace(src: str | Path, dst: str | Path) -> None:
        raise OSError("replace failed")

    monkeypatch.setattr(csv_filter.os, "replace", fake_replace)

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
            "--overwrite",
        ]
    )

    monkeypatch.setattr(csv_filter.os, "replace", real_replace)

    captured = capsys.readouterr()

    assert code == 1
    assert "could not write" in captured.err.lower()
    assert read_file(output_file) == "legacy\n"
    remaining_files = sorted(path.name for path in tmp_path.iterdir())
    assert "input.csv" in remaining_files
    assert "output.csv" in remaining_files
    assert len(remaining_files) == 2


def test_malformed_csv_raises_controlled_code_2(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, 'id,price\n1,"2\n')

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "invalid csv" in captured.err.lower() or "newline" in captured.err.lower()


def test_invalid_utf8_input_returns_code_2_without_traceback(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input_invalid_utf8.csv"
    output_file = tmp_path / "output.csv"
    input_file.write_bytes(b"id,price\n1,\x80\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "0",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "utf-8" in captured.err.lower()
    assert "traceback" not in captured.err.lower()


def test_input_and_output_hard_links_to_same_file_return_code_2(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_hardlink = tmp_path / "output_hardlink.csv"
    write_file(input_file, "id,price\n1,2\n")
    output_hardlink.hardlink_to(input_file)

    code = csv_filter.main(
        [
            str(input_file),
            str(output_hardlink),
            "--column",
            "price",
            "--threshold",
            "1",
            "--overwrite",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "different" in captured.err.lower()


def test_cleanup_failure_is_translated_to_controlled_code_1(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,2\n")

    real_replace = csv_filter.os.replace
    real_unlink = csv_filter.Path.unlink

    def fake_replace(src: str | Path, dst: str | Path) -> None:
        raise OSError("replace failed")

    def fake_unlink(self: Path, missing_ok: bool = False) -> None:
        raise PermissionError("cleanup denied")

    monkeypatch.setattr(csv_filter.os, "replace", fake_replace)
    monkeypatch.setattr(csv_filter.Path, "unlink", fake_unlink)

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
            "--overwrite",
        ]
    )

    monkeypatch.setattr(csv_filter.os, "replace", real_replace)
    monkeypatch.setattr(csv_filter.Path, "unlink", real_unlink)

    captured = capsys.readouterr()

    assert code == 1
    assert "could not clean temporary file" in captured.err.lower()


def test_expected_errors_do_not_print_traceback(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    write_file(input_file, "id,price\n1,abc\n")

    code = csv_filter.main(
        [
            str(input_file),
            str(output_file),
            "--column",
            "price",
            "--threshold",
            "1",
        ]
    )

    captured = capsys.readouterr()

    assert code == 2
    assert "traceback" not in captured.err.lower()
