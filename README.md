Inventory Management System - Version 4

Orverview

Inventory Management System is a console-based CRUD application developed in Pyhton 3.14.

The project manages products within a store inventory while progressively applying backend software engineering principles such as separation of responsibilities, domain validation and the Repository Pattern.

This version focuses on decoupling the business logic from the presistence mechanism, preparing the application for future storage implementations such as SQLite or PostgreSQL.

Problem Solved
The systm allowns a store to manage its inventory through the following operation

- Add a product
- List all products
- Search a product by ID
- Update product information
- Delete a product

Previous versions coupled the service layer directly to JSON persistence.

Version 4 solves this problem by introducing a repository abstraction, allowing the service layer to work independently of the storage technology.

Architecture
The project follows a layered architecture based on separation of responsibilities.

Console Interface
        │
        ▼
InventoryService
        │
        ▼
ProductRepository (Contract)
       ▲
       │
 ┌───────────────┐
 │               │
 ▼               ▼
JSONProductRepository
InMemoryProductRepository
        │
        ▼
    Persistence

The Repository Patterns acts as the gateway to the collection of products, hiding the persistence implementation from the service layer.

Project Layers

Domain: Contains the business model.

- Product
- Domain validations
- Domain exceptions

The domain guarantees that every Product is always valid.

Repository: Responsible for accesing the collection of products

The repository defines the operations required by the application without exposing how the data is stored.

Repository contract:

- add()
- get_by_id()
- list_all()
- update()
- delete()

Current implementations:

- JSONProductRepository
- InMemoryProductRepository

Service

Contains the application use cases.

Responsibilities:

- Coordinate business operations.
- Use the repository.
- Never manipulate JSON directly.

The service does not know where the data comes from.

Interface

Console menu.

Responsibilities:

- Receive user input.
- Display information.
- Call the appropriate service methods.

The interface contains no business logic.

Technologies

- Python 3.14
- Object-Oriented Programming
- Repository Pattern
- JSON persistence
- Type hints
- Abstract Base Classes (ABC)

Development Setup

Create and activate the Python 3.14 virtual environment:

```bash
python3.14 -m venv venv
source venv/bin/activate
```

Install the development dependency group:

```bash
python -m pip install --group dev
```

Run the active-code quality check:

```bash
python -m ruff check .
```

Run the test suite once the `tests/` directory is introduced:

```bash
python -m pytest
```

What I Learned

During this version I learned how to:

- Separate business logic from persistence.
- Apply the Repository Pattern.
- Work with Abstract Base Classes.
- Design contracts using abstract methods.
- Inject dependencies into the service layer.
- Reduce coupling between application layers.
- Build a cleaner backend architecture.
- Understand that the repository is the gateway to the collection of domain entities rather than the JSON file itself.

Future Improvements (Version 5)

The next version will focus on software quality.

Planned improvements:

- Unit tests for the domain.
- Unit tests for the service layer using the in-memory repository.
- Pytest test suite.
- DTOs for data transfer.
- Custom logging.
- Dependency injection improvements.
- SQLite repository implementation.
- Documentation expansion.
- Preparation for migration to Django or FastAPI.

Educational Goal

This project is part of a backend learning roadmap.

The objective is not only to build a CRUD application but also to understand how professional backend applications separate responsibilities, isolate persistence, and remain maintainable as they evolve.
