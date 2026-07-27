from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from decimal import Decimal, InvalidOperation
from pathlib import Path


class CSVFilterError(Exception):
    """Base exception for expected CSV filter errors."""


class CSVArgumentsError(CSVFilterError):
    """Raised when CLI arguments are invalid for this utility."""


class CSVHeaderError(CSVFilterError):
    """Raised when the CSV header is invalid."""


class CSVDataError(CSVFilterError):
    """Raised when CSV row data is invalid."""


class CSVIOError(CSVFilterError):
    """Raised when I/O or filesystem operations fail."""


def _cleanup_file(path: Path, *, label: str) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError as error:
        raise CSVIOError(f"Could not clean {label}: {path}") from error


def parse_finite_decimal(
    text: str,
    *,
    field_name: str,
    error_cls: type[CSVFilterError],
) -> Decimal:
    value = text.strip()
    if value == "":
        raise error_cls(f"{field_name} must not be empty")

    try:
        decimal_value = Decimal(value)
    except InvalidOperation as error:
        raise error_cls(f"{field_name} must be a valid decimal number") from error

    if not decimal_value.is_finite():
        raise error_cls(f"{field_name} must be finite")

    return decimal_value


def is_strictly_greater(value: Decimal, threshold: Decimal) -> bool:
    return value > threshold


def read_and_filter_csv(
    input_path: Path,
    *,
    column_name: str,
    threshold: Decimal,
) -> tuple[list[str], list[list[str]]]:
    try:
        with input_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=",", strict=True)

            try:
                header = next(reader)
            except StopIteration as error:
                raise CSVHeaderError("CSV input is empty") from error

            if not header:
                raise CSVHeaderError("CSV header is required")

            if any(name.strip() == "" for name in header):
                raise CSVHeaderError("CSV header contains empty column names")

            if len(set(header)) != len(header):
                raise CSVHeaderError("CSV header contains duplicate column names")

            try:
                column_index = header.index(column_name)
            except ValueError as error:
                raise CSVHeaderError(f"Column not found: {column_name}") from error

            filtered_rows: list[list[str]] = []
            expected_fields = len(header)

            for line_number, row in enumerate(reader, start=2):
                if not row:
                    raise CSVDataError(f"Row {line_number} is empty")

                if len(row) != expected_fields:
                    fields_count = len(row)
                    raise CSVDataError(
                        f"Row {line_number} has {fields_count} fields, "
                        f"expected {expected_fields}"
                    )

                value_text = row[column_index]
                value = parse_finite_decimal(
                    value_text,
                    field_name=f"Row {line_number}, column '{column_name}'",
                    error_cls=CSVDataError,
                )
                if is_strictly_greater(value, threshold):
                    filtered_rows.append(row)

            return header, filtered_rows

    except FileNotFoundError as error:
        raise CSVIOError(f"Input file was not found: {input_path}") from error
    except UnicodeDecodeError as error:
        raise CSVDataError("Input CSV must be valid UTF-8") from error
    except PermissionError as error:
        raise CSVIOError(f"Input file cannot be accessed: {input_path}") from error
    except OSError as error:
        raise CSVIOError(f"Could not read input file: {input_path}") from error
    except csv.Error as error:
        raise CSVDataError(f"Invalid CSV input: {error}") from error


def write_csv_atomic(
    output_path: Path,
    *,
    header: list[str],
    rows: list[list[str]],
    overwrite: bool,
) -> None:
    output_dir = output_path.parent
    temp_path: Path | None = None

    try:
        if not overwrite and output_path.exists():
            if output_path.is_dir():
                raise CSVIOError(f"Output path is a directory: {output_path}")
            raise CSVArgumentsError(
                "Output file already exists. Use --overwrite to replace it"
            )

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=output_dir,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            writer = csv.writer(temp_file, delimiter=",")
            writer.writerow(header)
            writer.writerows(rows)

        if overwrite:
            os.replace(temp_path, output_path)
            temp_path = None
        else:
            os.replace(temp_path, output_path)
            temp_path = None
    except FileNotFoundError as error:
        raise CSVIOError(f"Output directory was not found: {output_dir}") from error
    except FileExistsError as error:
        raise CSVArgumentsError(
            "Output file already exists. Use --overwrite to replace it"
        ) from error
    except PermissionError as error:
        raise CSVIOError(f"Output file cannot be written: {output_path}") from error
    except OSError as error:
        raise CSVIOError(f"Could not write output file: {output_path}") from error
    except csv.Error as error:
        raise CSVIOError(f"Could not serialize CSV output: {error}") from error
    finally:
        cleanup_error: CSVIOError | None = None

        if temp_path is not None and temp_path.exists():
            try:
                _cleanup_file(temp_path, label="temporary file")
            except CSVIOError as error:
                cleanup_error = error

        if cleanup_error is not None:
            raise cleanup_error


def ensure_distinct_paths(input_path: Path, output_path: Path) -> None:
    if input_path.resolve() == output_path.resolve():
        raise CSVArgumentsError("Input and output must be different files")

    if input_path.exists() and output_path.exists():
        try:
            if input_path.samefile(output_path):
                raise CSVArgumentsError("Input and output must be different files")
        except OSError:
            # If metadata cannot be read, this check should not hide the later
            # filesystem error handling in the main workflow.
            pass


def run_filter(
    input_path: Path,
    output_path: Path,
    *,
    column_name: str,
    threshold_text: str,
    overwrite: bool,
) -> None:
    ensure_distinct_paths(input_path, output_path)
    threshold = parse_finite_decimal(
        threshold_text,
        field_name="Threshold",
        error_cls=CSVArgumentsError,
    )

    header, filtered_rows = read_and_filter_csv(
        input_path,
        column_name=column_name,
        threshold=threshold,
    )

    write_csv_atomic(
        output_path,
        header=header,
        rows=filtered_rows,
        overwrite=overwrite,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inventory_csv_filter.py",
        description="Filter CSV rows by numeric column greater than a threshold",
    )
    parser.add_argument("input", help="Input CSV file path")
    parser.add_argument("output", help="Output CSV file path")
    parser.add_argument("--column", required=True, help="Column name to evaluate")
    parser.add_argument(
        "--threshold",
        required=True,
        help="Rows with values greater than this threshold are kept",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing an existing output file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        run_filter(
            Path(args.input),
            Path(args.output),
            column_name=args.column,
            threshold_text=args.threshold,
            overwrite=args.overwrite,
        )
    except CSVIOError as error:
        print(error, file=sys.stderr)
        return 1
    except (CSVArgumentsError, CSVHeaderError, CSVDataError) as error:
        print(error, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
