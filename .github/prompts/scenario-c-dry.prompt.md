# Escenario C — Refactorización DRY de la consola de Inventory

## Rol y forma de colaboración

Actúa como desarrollador backend senior especializado en aplicaciones de
consola y como tutor técnico. Ayuda al programador a analizar, caracterizar,
refactorizar y verificar la solución sin sustituir su criterio. Explica en
español las decisiones, los límites de DRY, los compromisos técnicos y la
evidencia de verificación. Conserva los identificadores Python y todos los
mensajes observables en su idioma actual.

El programador conserva la responsabilidad de autorizar la implementación,
aceptar el resultado y decidir cualquier cambio de contrato. No edites ningún
archivo hasta completar la puerta de entorno, inspeccionar el estado actual,
presentar la tarjeta de preautorización y recibir una autorización explícita
que coincida con el alcance propuesto.

La existencia de este prompt representa únicamente la autorización de la fase
C1: creación y revisión del propio prompt. No autoriza pruebas ni cambios en
`inventory_v4.py`.

## Contexto obligatorio del repositorio

Antes de analizar el escenario, lee por completo:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.github/instructions/python.instructions.md`
- `.github/instructions/tests.instructions.md`
- `inventory_v4.py`
- `pyproject.toml`

Respeta todas sus instrucciones. En particular:

- `inventory_v4.py` es la línea base activa y la única versión de Inventory que
  puede evolucionar.
- `inventory.py`, `inventory_v2.py` e `inventory_v3.py` son artefactos
  históricos. No los modifiques, formatees, renombres ni sincronices con V4.
- Preserva cualquier cambio local ajeno al escenario. No lo limpies, reviertas,
  añadas a staging ni incluyas en un commit.
- `Product` protege las invariantes del dominio.
- `InventoryService` contiene los casos de uso y depende del contrato
  `ProductRepository`.
- `ProductRepository` es el puerto de persistencia.
- `InMemoryProductRepository` y `JSONproductRepository` son adaptadores de
  infraestructura.
- Las funciones de consola y `main()` contienen interacción, presentación,
  orquestación y composición.

## Puerta obligatoria de entorno y documentación

Antes de analizar o implementar:

1. Activa el entorno virtual documentado por el proyecto:

   ```text
   source venv/bin/activate
   ```

2. Ejecuta:

   ```text
   python --version
   ```

3. Confirma que el resultado es Python 3.14.x.
4. Confirma que todas las URLs de documentación consultadas contienen
   explícitamente `/3.14/`.
5. Si el intérprete no es Python 3.14.x o alguna URL no pertenece a `/3.14/`,
   detente y comunica la discrepancia. No analices el código como si un fallo de
   entorno fuese un defecto de la aplicación.

No instales, actualices ni reemplaces Python, el entorno virtual o sus
dependencias para superar esta puerta.

## Documentación oficial permitida

Utiliza exclusivamente documentación oficial versionada de Python 3.14. No
uses rutas `/3/`, `/latest/`, `/3.12/` ni documentación de terceros.

Fuentes autorizadas:

- [Definiciones de funciones — Python 3.14](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions)
- [Sentencia `try` — Python 3.14](https://docs.python.org/3.14/reference/compound_stmts.html#the-try-statement)
- [`collections.abc.Callable` — Python 3.14](https://docs.python.org/3.14/library/collections.abc.html#collections.abc.Callable)

La documentación sobre definiciones de funciones se puede usar para verificar:

- cómo se definen funciones y parámetros;
- que una definición crea un objeto función y que el cuerpo se ejecuta cuando
  se llama;
- la sintaxis de las anotaciones de parámetros y retorno;
- el uso de funciones como objetos que pueden asignarse y posteriormente
  invocarse.

La documentación de `try` se puede usar para verificar:

- el comportamiento de `try` y `except`;
- el orden y la coincidencia de los manejadores;
- la propagación de una excepción cuando ningún `except` coincide;
- la continuación de la ejecución después de una captura.

Consulta la documentación de `collections.abc.Callable` únicamente si el diseño
propuesto y posteriormente aprobado utiliza un dispatcher que almacena
funciones manejadoras. `Callable` es opcional y no debe convertirse en un
requisito artificial.

Estas fuentes describen el lenguaje y la biblioteca estándar. No establecen la
arquitectura de Inventory, no exigen manejadores, no definen cómo aplicar DRY y
no autorizan a cambiar la política de excepciones. Las decisiones
arquitectónicas proceden del código actual, las instrucciones del repositorio y
el contrato aprobado. No atribuyas esas decisiones a la documentación de
Python.

Si necesitas otra fuente para justificar una afirmación técnica, detente y
solicita autorización antes de consultarla. No inventes garantías ni sustituyas
una URL versionada por otra.

## Objetivo autorizado del escenario

Aplicar el principio DRY (*Don't Repeat Yourself*) mediante funciones pequeñas
y reutilizables, sin alterar la lógica original.

La futura refactorización afecta exclusivamente a:

- la interfaz de consola de `inventory_v4.py`;
- la orquestación y composición de `inventory_v4.py`;
- una suite de caracterización de esa interfaz.

La tarea consiste en reorganizar cómo `main()`:

- recibe y valida entradas mediante las funciones de consola existentes;
- selecciona una opción;
- llama a `InventoryService`;
- traduce resultados o excepciones a salida de consola;
- repite el menú hasta seleccionar la opción `0`.

No se añade ninguna operación de negocio. DRY no significa fusionar casos de
uso distintos. Centraliza solo comportamiento realmente repetido y conserva
explícita la política particular de cada opción.

## Capas y responsabilidades autorizadas

### Interfaz de consola

Se permite extraer el comportamiento de cada opción del menú a una función
manejadora. Cada manejador puede:

1. recopilar entradas mediante las funciones de consola;
2. invocar el método público correspondiente de `InventoryService`;
3. traducir el resultado o una excepción esperada a la salida actual.

Un manejador pertenece a la interfaz. No implementa el caso de uso, no valida
invariantes de dominio y no conoce detalles de persistencia.

### Orquestación y composición

`main() -> None` debe seguir siendo el *composition root* que crea:

```text
JSONproductRepository("inventory_data.json")
InventoryService(repository)
```

Se permite delegar el bucle del menú en una función que reciba
`InventoryService`. Se permite un dispatcher sencillo de funciones si elimina
duplicación sin ocultar el flujo; no es obligatorio.

### Pruebas de interfaz

Antes de refactorizar producción, se debe crear una suite de caracterización que
pase contra la línea base sin modificar. Debe observar la colaboración entre la
consola y un servicio controlado. Probar que la consola llama al servicio no
equivale a volver a probar la lógica interna del servicio.

## Archivos permitidos en una futura implementación

Una autorización posterior del escenario C puede permitir exclusivamente:

- modificar `inventory_v4.py`;
- crear `tests/test_inventory_v4_console.py`.

No crees, edites, muevas, formatees ni elimines ningún otro archivo. En
particular, quedan fuera de alcance:

- `Product`;
- `InventoryService`;
- `ProductRepository`;
- `InMemoryProductRepository`;
- `JSONproductRepository`;
- `inventory_data.json`;
- `inventory.py`;
- `inventory_v2.py`;
- `inventory_v3.py`;
- `inventory_csv_filter.py`;
- `tests/test_inventory_csv_filter.py`;
- `pyproject.toml`;
- cualquier archivo de instrucciones o prompt;
- el entorno virtual y los archivos de dependencias.

Aunque `inventory_v4.py` sea un archivo permitido, dentro de él solo pueden
cambiar la interfaz de consola y la orquestación. La autorización del archivo no
amplía las capas autorizadas.

## Dependencias

No se introduce ninguna dependencia nueva de producción.

Se permite la biblioteca estándar. `collections.abc.Callable` puede usarse
únicamente si el diseño aprobado necesita anotar un dispatcher de funciones;
no es una dependencia externa.

Dependencias de desarrollo ya existentes y suficientes:

- `pytest`;
- `monkeypatch`, proporcionado por pytest;
- `capsys`, proporcionado por pytest;
- Ruff, ya configurado en `pyproject.toml`.

No se necesita ni se autoriza:

- una librería de CLI;
- un framework de inyección de dependencias;
- una librería de mocks;
- una herramienta nueva de cobertura;
- clases para representar comandos;
- decoradores de registro;
- un Command Pattern basado en clases.

Si la solución parece requerir otra dependencia, detente, justifícala y solicita
una nueva autorización. No la instales ni modifiques `pyproject.toml`.

## Diseño permitido, no obligatorio

El análisis puede proponer funciones pequeñas semejantes a:

```text
run_inventory_menu(service)
handle_add_product(service)
handle_list_products(service)
handle_find_product(service)
handle_rename_product(service)
handle_update_price(service)
handle_update_stock(service)
handle_delete_product(service)
render_expected_error(error)
```

Los nombres definitivos y cualquier helper adicional deben justificarse en la
tarjeta de preautorización. No fuerces `render_expected_error()` si mezclaría
políticas distintas, ni un dispatcher si una selección explícita resulta más
clara.

Todas las funciones nuevas deben tener una responsabilidad concreta y
anotaciones de tipo. Evita abstracciones especulativas, capas nuevas y helpers
que solo reubiquen una única línea sin eliminar duplicación real.

No uses `except Exception` ni un manejador global que capture fallos de
programación. No amplíes ni reduzcas accidentalmente qué excepciones captura
cada opción. Las excepciones no manejadas actualmente deben seguir
propagándose.

## Contrato público y observable que debe preservarse

### API y persistencia

No cambies:

- constructores, propiedades, métodos o excepciones de `Product`;
- firmas, argumentos, retornos o excepciones de `InventoryService`;
- métodos del contrato `ProductRepository`;
- comportamiento de los repositorios concretos;
- formato, ruta predeterminada o contenido de `inventory_data.json`;
- firma `main() -> None`;
- implementación JSON creada por `main()`.

### Menú

Conserva exactamente el contenido, el orden, la puntuación y el salto inicial:

```text

=== INVENTORY SYSTEM V4 ===
1. Add product.
2. List products.
3. Finds product by ID.
4. Rename product.
5. Update product price.
6. Update product stock.
7. Delete product.
0. Exit.
```

Conserva:

- el prompt `Choose an option: `;
- las opciones válidas de `"0"` a `"7"`;
- `Invalid option` ante una opción inválida;
- el reintento hasta obtener una opción válida;
- la repetición del menú después de cada operación;
- `Exiting inventory system.` y la terminación al seleccionar `0`.

### Helpers de entrada

Conserva firmas, limpieza con `strip()`, reintentos y mensajes:

- `ask_option() -> str`;
- `ask_non_empty_text(message: str) -> str`;
- `ask_positive_int(message: str) -> int`;
- `ask_positive_float(message: str) -> float`;
- `It cannot be empty`;
- `The value must be zero or greater.`;
- `Invalid number.`.

No cambies la aceptación actual del valor cero ni aproveches el refactor para
resolver decisiones numéricas pendientes como `bool`, `NaN` o infinito.

### Opción 1 — Alta

Conserva, en este orden:

```text
"Product ID: "
"Product name: "
"Product price: "
"Stock quantitty: "
```

Conserva la llamada:

```text
service.add_product(
    product_id=product_id,
    name=name,
    price=price,
    stock_quantity=stock_quantity,
)
```

Conserva `Product added successfully.`. Mantén las traducciones actuales:

- `ProductAlreadyExistsError` → `print(error)`;
- `InventoryStorageError` → prefijo `Storage error: `;
- `TypeError` y `ValueError` → prefijo `Invalid product data: `.

### Opción 2 — Listado

Conserva `service.list_products()` y `print(products)`. No lo sustituyas por
`print_products(products)` ni cambies la representación, aunque el helper ya
exista. Conserva `Storage error: ` para `InventoryStorageError`.

### Opción 3 — Búsqueda por ID

Conserva:

- `Product ID: `;
- `service.find_product_by_id(product_id)`;
- `print(product)`;
- `ProductNotFoundError` mediante `print(error)`;
- `InventoryStorageError` con el prefijo `Storage error: `.

### Opción 4 — Renombrado

Conserva, en este orden:

```text
"Product ID: "
"New product name: "
```

Conserva `service.rename_product(product_id, new_name)` y el mensaje actual
`Stock renamed successfully.`, aunque su redacción sea mejorable. Conserva:

- `ProductNotFoundError` mediante `print(error)`;
- `InventoryStorageError` con `Storage error: `;
- `TypeError` y `ValueError` con `Invalid product data: `.

### Opción 5 — Actualización de precio

Conserva, en este orden:

```text
"Product ID: "
"New price: "
```

Conserva:

- `service.update_price(product_id, new_price)`;
- `Product price updated successfully.`;
- `ProductNotFoundError` mediante `print(error)`;
- `InventoryStorageError` con `Storage error: `;
- `TypeError` y `ValueError` con `Invalid product data: `.

### Opción 6 — Actualización de stock

Conserva, en este orden:

```text
"Product ID: "
"New stock quantity: "
```

Conserva:

- `service.update_stock(product_id, new_stock_quantity)`;
- `Product stock updated successfully.`;
- `ProductNotFoundError` mediante `print(error)`;
- `InventoryStorageError` con `Storage error: `;
- `TypeError` y `ValueError` con `Invalid product data: `.

### Opción 7 — Eliminación

Conserva:

- `Product ID: `;
- `service.delete_product(product_id)`;
- `Product deleted successfully.`;
- `ProductNotFoundError` mediante `print(error)`;
- `InventoryStorageError` con `Storage error: `.

### Comportamientos imperfectos congelados

Esta es una refactorización estructural. No corrijas simultáneamente:

- `Stock quantitty: `;
- `Stock renamed successfully.`;
- `3. Finds product by ID.`;
- el uso de `print(products)` en la opción 2;
- ninguna otra errata, representación o inconsistencia existente.

Registra esas observaciones, si son relevantes, como deuda técnica fuera de
alcance. Corregirlas exige otro escenario y otra autorización.

## Reglas de negocio protegidas

La refactorización debe cambiar estructura, no comportamiento.

Permanecen en sus capas actuales y sin modificación:

- ID de producto único;
- ID, nombre, precio y stock válidos;
- tratamiento de producto inexistente;
- coherencia de las actualizaciones y eliminaciones;
- persistencia JSON;
- traducción de fallos de almacenamiento;
- dirección de dependencias entre dominio, aplicación, puerto e
  infraestructura.

Los manejadores no pueden duplicar ni mover estas reglas. Deben limitarse a
adaptar una acción de consola al contrato público de `InventoryService`.

## Ausencia expresa de requisitos adicionales

Este escenario no contiene requisitos de:

- concurrencia, paralelismo, hilos, procesos, `asyncio`, funciones `async` ni
  bloqueos;
- nuevas opciones de menú;
- nuevas operaciones de negocio;
- cambios de persistencia;
- cambio de formato de salida;
- internacionalización;
- logging, telemetría o métricas;
- configuración externa;
- optimización de rendimiento;
- corrección general de deuda técnica;
- rediseño del dominio o del servicio;
- ampliación funcional de los helpers de entrada.

No implementes mejoras “aprovechando” el refactor.

## Pruebas de aceptación de una futura implementación

### Orden obligatorio

1. Escribe `tests/test_inventory_v4_console.py` contra la línea base.
2. Ejecuta la suite nueva y confirma que pasa antes de cambiar
   `inventory_v4.py`.
3. Refactoriza únicamente después de obtener esa caracterización verde.
4. Ejecuta las mismas pruebas después del refactor.
5. No cambies expectativas para adaptar las pruebas a una diferencia provocada
   por la nueva estructura.

### Aislamiento

Las pruebas deben:

- usar pytest;
- sustituir entradas de consola con `monkeypatch`;
- capturar salida con `capsys`;
- evitar por completo el archivo JSON real;
- controlar la creación o colaboración de `InventoryService` mediante fakes
  sencillos escritos en la propia prueba o monkeypatch;
- ejecutar `main()` para caracterizar el contrato externo;
- ser deterministas e independientes del orden de ejecución;
- no acceder a red ni depender del estado del inventario real.

No añadas una librería de mocks. No hagas aserciones innecesarias sobre nombres
privados de handlers o sobre la forma concreta del dispatcher.

### Casos mínimos

La suite debe demostrar, antes y después del refactor:

- opción inválida: muestra `Invalid option` y vuelve a solicitarla;
- opción `0`: muestra el mensaje de salida y termina;
- opción `1`: recopila los cuatro valores, llama a `add_product()` con nombres y
  valores exactos y muestra el éxito;
- opción `2`: llama a `list_products()` e imprime la lista con el comportamiento
  actual de `print(products)`;
- opción `3`: llama a `find_product_by_id()` con el ID exacto e imprime el
  producto;
- opción `4`: llama a `rename_product()` con argumentos exactos y conserva
  `Stock renamed successfully.`;
- opción `5`: llama a `update_price()` con argumentos exactos;
- opción `6`: llama a `update_stock()` con argumentos exactos;
- opción `7`: llama a `delete_product()` con el ID exacto;
- cada operación vuelve al menú y permite salir mediante `0`;
- las entradas vacías, negativas o no numéricas mantienen sus reintentos y
  mensajes actuales;
- `ProductAlreadyExistsError`, donde actualmente aplica, mantiene
  `print(error)`;
- `ProductNotFoundError`, donde actualmente aplica, mantiene `print(error)`;
- `InventoryStorageError`, en cada opción que actualmente lo captura, mantiene
  el prefijo `Storage error: `;
- `TypeError` y `ValueError`, solo donde actualmente se traducen, mantienen
  `Invalid product data: `;
- las excepciones no capturadas por la línea base no quedan ocultas por un
  `except` más amplio.

Cada prueba debe seleccionar la operación necesaria y después `0`, salvo cuando
esté verificando de forma deliberada una excepción que deba propagarse.

## Flujo obligatorio de trabajo

### Fase 1 — Análisis y preautorización

Después de superar la puerta de entorno:

1. Confirma la rama actual y ejecuta `git status --short`.
2. Si existen cambios locales, descríbelos y determina si puedes continuar sin
   tocarlos. Detente si se solapan con los archivos del escenario.
3. Inspecciona en modo de solo lectura la interfaz y la orquestación de
   `inventory_v4.py`.
4. Identifica duplicación real, diferencias entre opciones y límites actuales
   de los bloques `try`/`except`.
5. Propón el conjunto mínimo de funciones, sus firmas anotadas y su
   responsabilidad. Indica si propones un dispatcher y, en ese caso, por qué
   `Callable` aporta claridad.
6. Presenta una tarjeta de preautorización concreta que responda:

   1. ¿Qué capa se modifica?
   2. ¿Por qué se modifica esa capa?
   3. ¿Qué dependencia se introduce?
   4. ¿Qué contrato se mantiene?
   5. ¿Qué regla de negocio se protege?
   6. ¿Qué test demostrará que funciona?

7. Confirma expresamente que el alcance se limita a modificar
   `inventory_v4.py` y crear `tests/test_inventory_v4_console.py`.
8. Explica cómo las pruebas pasarán contra la línea base antes del refactor y
   cómo evitarán `inventory_data.json`.
9. Señala cualquier ambigüedad que todavía pertenezca al programador.

En esta fase no edites, crees, muevas, formatees ni elimines archivos. No
instales dependencias ni ejecutes comandos que modifiquen datos. Termina con:

```text
Esperando autorización explícita para implementar el escenario C.
```

Después, detente.

### Puerta de autorización

Continúa únicamente si el programador autoriza expresamente una tarjeta cuyo
alcance coincide con este prompt. La autorización debe cubrir tanto la suite de
caracterización como la refactorización, respetando el orden pruebas primero.

Si el programador cambia el diseño o si el trabajo exige otra capa, archivo,
dependencia, firma, excepción, regla, mensaje, prueba aceptada o comportamiento
observable, actualiza la tarjeta y vuelve a esperar una autorización.

### Fase 2 — Caracterización autorizada

1. Crea únicamente `tests/test_inventory_v4_console.py`.
2. Implementa la suite mínima que cubra las pruebas de aceptación.
3. No modifiques todavía `inventory_v4.py`.
4. Ejecuta la selección de pruebas de consola.
5. Si una prueba falla contra la línea base, determina si la expectativa
   contradice el comportamiento actual. No modifiques producción ni debilites
   la prueba sin presentar la evidencia al programador y obtener una decisión.
6. Continúa a la refactorización solo cuando la caracterización autorizada pase.

### Fase 3 — Refactorización autorizada

1. Modifica exclusivamente la interfaz y la orquestación de
   `inventory_v4.py`.
2. Conserva `main()` como *composition root*.
3. Extrae funciones pequeñas solo para eliminar duplicación real y hacer
   explícita cada opción.
4. Mantén la política específica de excepciones; no uses `except Exception`.
5. No cambies la suite de caracterización para acomodar regresiones.
6. Ejecuta todas las verificaciones requeridas.
7. Inspecciona el diff para confirmar que no existen cambios fuera del alcance.
8. No añadas archivos a staging, no crees commits y no hagas push sin una
   autorización posterior y explícita.

## Criterios automáticos de rechazo

Detén el trabajo y considera la propuesta o implementación rechazada si ocurre
cualquiera de estas condiciones:

- `python --version` no devuelve Python 3.14.x;
- se consulta una URL que no contiene `/3.14/`;
- se modifica o crea un archivo distinto de los dos permitidos para la futura
  implementación;
- se cambia dominio, servicio, puerto, repositorios o persistencia;
- se modifica una firma pública, excepción, retorno o llamada de servicio;
- cambia cualquier texto, prompt, orden, reintento o representación observable;
- se corrige una errata congelada;
- se añade una operación o mejora funcional;
- se introduce una dependencia o se modifica el entorno;
- se añade concurrencia o asincronía;
- se implementan clases de comandos, decoradores de registro o Command Pattern;
- se captura `Exception` de forma amplia o se oculta un fallo que antes se
  propagaba;
- los handlers acceden directamente a un repositorio o a JSON;
- se mueven o duplican reglas de negocio en la consola;
- las pruebas leen o modifican `inventory_data.json`;
- se modifica, elimina, omite, marca `xfail` o debilita una prueba para obtener
  un resultado verde;
- se modifica producción antes de tener caracterización verde;
- no se recibe la autorización explícita exigida;
- se incluye trabajo ajeno al escenario en staging, commit o push;
- se intenta instalar una herramienta para superar una limitación del entorno.

Ante un rechazo, comunica la evidencia exacta y espera una decisión. No
expandas el alcance por iniciativa propia.

## Verificación requerida

Con el entorno `venv` activado, ejecuta y comunica los resultados exactos:

```text
python --version
python -m pytest tests/test_inventory_v4_console.py
python -m pytest
python -m ruff check inventory_v4.py tests/test_inventory_v4_console.py
git diff --check
git status --short
```

Si un comando no está disponible, informa de la limitación. No instales ni
cambies el entorno sin autorización.

Antes de declarar el escenario terminado, compara el resultado de la suite de
caracterización antes y después del refactor. Confirma que el diff solo afecta
los archivos y las responsabilidades autorizadas.

## Formato del informe final

Informa:

- archivos y capas modificados;
- funciones extraídas y duplicación eliminada;
- dependencias, indicando explícitamente que no hubo cambios si corresponde;
- contrato observable y reglas de negocio preservados;
- pruebas ejecutadas antes y después del refactor;
- comandos de calidad y resultados exactos;
- riesgos, verificaciones fallidas o decisiones que siguen perteneciendo al
  programador.

No hagas staging, commit ni push como parte de este escenario salvo autorización
expresa posterior.
