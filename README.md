# Inventory Management System · V4

Aplicación de consola para gestionar productos de un inventario, desarrollada
como proyecto de aprendizaje de backend con Python 3.14.

El proyecto muestra la evolución desde un CRUD hasta una arquitectura con
validaciones de dominio, servicios, repositorios intercambiables y pruebas
automatizadas. **La versión activa es `inventory_v4.py`.** Las versiones
anteriores se conservan como historial del aprendizaje.

## Funcionalidades

- Crear, listar, buscar por ID y eliminar productos.
- Actualizar nombre, precio y cantidad de stock.
- Validar identificadores y cantidades no negativos y nombres no vacíos.
- Detectar IDs duplicados y productos inexistentes mediante excepciones propias.
- Guardar y recuperar productos en JSON.
- Usar un repositorio en memoria para aislar las pruebas del servicio.

También incluye [`inventory_csv_filter.py`](inventory_csv_filter.py), una
utilidad independiente para filtrar un CSV por una columna numérica y conservar
las filas cuyo valor sea estrictamente mayor que un umbral. Valida los datos
antes de escribir y requiere `--overwrite` para reemplazar una salida existente.

## Arquitectura

Las capas están agrupadas en un único módulo para facilitar su estudio:

```text
Consola → InventoryService → ProductRepository (contrato)
                                  ↑
                         implementado por
                     ┌────────────┴─────────────┐
        InMemoryProductRepository     JSONproductRepository
```

- **Dominio:** `Product` protege sus invariantes.
- **Aplicación:** `InventoryService` coordina los casos de uso.
- **Puerto:** `ProductRepository` declara `add`, `get_by_id`, `list_all`,
  `update` y `delete`.
- **Infraestructura:** repositorios en memoria y JSON.
- **Interfaz:** funciones de consola y `main()`, donde se inyecta el repositorio.

El servicio depende del contrato del repositorio. La implementación JSON
utiliza `inventory_data.json` en el directorio desde el que se ejecuta el programa.

## Instalación y ejecución

Requiere Python 3.14. La aplicación utiliza exclusivamente la biblioteca estándar;
pytest y Ruff son herramientas de desarrollo.

Desde la raíz del proyecto, en macOS o Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install --group dev
python inventory_v4.py
```

En Windows, activa el entorno con `.venv\Scripts\Activate.ps1` desde PowerShell.

Para consultar la utilidad CSV:

```bash
python inventory_csv_filter.py --help
```

Ejemplo con un CSV propio que contenga la columna `stock_quantity`:

```bash
python inventory_csv_filter.py entrada.csv salida.csv --column stock_quantity --threshold 10
```

## Pruebas y calidad

```bash
python3 -m pytest -q
python -m ruff check .
```

La suite incluye pruebas de dominio, servicio, repositorio en memoria, consola
y utilidad CSV. El **21 de septiembre de 2026**, la ejecución local con Python
3.14.0 obtuvo **127 pruebas correctas**. Esta cifra describe esa revisión del
código y no implica cobertura completa de todos los escenarios de persistencia.

## Qué he practicado

- Separación de responsabilidades y dirección de las dependencias.
- Repository Pattern, clases abstractas e inyección de dependencias.
- Validación de entidades y manejo explícito de errores.
- Pruebas de casos de uso con almacenamiento en memoria.
- Refactorización de la consola conservando su comportamiento observable.
- Procesamiento de archivos CSV y pruebas de fallos de entrada/salida.

## Alcance y evolución

Es un proyecto educativo de consola. No implementa una API web ni repositorios
SQLite o PostgreSQL. Las pruebas ya forman parte de V4; no son una funcionalidad
futura reservada para V5.

Los archivos `inventory.py`, `inventory_v2.py` e `inventory_v3.py` documentan
etapas anteriores y no son el punto de entrada de la versión actual.
