# Coding Guidelines

## Python Version

All code must be compatible with Python 3.12.

## Type Hinting

- Use the `typing` library as little as possible.
- For `list`, `dict`, and `tuple`, use the lowercase built-in type hints: `list`, `dict`, `tuple`.
- For unions, use the `|` operator (e.g., `str | int`).
- For optional types, use `| None` (e.g., `str | None`).

## Package Management

- Packages are managed using `uv`.
- To add a new package, run: `uv add <package-name>`
- To install required packages, run: `uv sync`
- To run a script, use: `uv run <script-name>`

## Code Style

- All code should follow PEP 8 and other relevant PEP standards.