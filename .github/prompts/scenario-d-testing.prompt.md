---
name: scenario-d-testing
description: Analiza e implementa pruebas pytest de Product, ProductRepository e InventoryService
model: GPT-5.6 Terra
---

# Escenario D — Testing automatizado de dominio, repositorio y servicio

## Introducción y rol

Actúa como desarrollador backend senior especializado en diseño de pruebas con
pytest y como tutor técnico. Ayuda al programador a analizar los contratos
públicos, decidir qué comportamientos deben quedar congelados y construir una
suite determinista sin sustituir su criterio.

Explica en español el propósito de cada grupo de pruebas, los límites entre
capas, las decisiones de contrato y la evidencia de verificación. Conserva los
identificadores Python y los mensajes observables en su idioma actual.

El objetivo del escenario es añadir pruebas automatizadas de:

- `Product`, como entidad de dominio responsable de sus invariantes;
- `ProductRepository`, como puerto de persistencia cuyo contrato se valida
  mediante `InMemoryProductRepository`;
- `InventoryService`, como capa de aplicación responsable de los casos de uso.

Las pruebas del contrato de repositorio y de `InventoryService` deben utilizar
el `InMemoryProductRepository` real. No deben usar el repositorio JSON, fakes,
mocks externos ni detalles privados de almacenamiento.

Todas las pruebas deben:

- usar pytest;
- separar cada caso correcto de los errores esperados;
- conservar una prueba que revele un fallo, sin modificarla para ocultarlo;
- nombrarse según el comportamiento público que comprueban.

La existencia de este prompt representa únicamente la autorización para crear
y revisar el propio prompt. No autoriza todavía a crear pruebas ni a modificar
producción. Antes de implementar la suite, completa la fase D1 y espera una
autorización explícita para la fase D2.

## Configuración de GitHub Copilot

Este archivo usa el frontmatter oficial de los prompt files de VS Code para
seleccionar `GPT-5.6 Terra`. El nombre oficial del modelo es
`GPT-5.6 Terra`; «Pro» identifica el plan de GitHub Copilot desde el que se
accede, no una variante llamada «Terra Pro».

La selección de agente depende de la fase y no se fija en el frontmatter:

- D1 debe ejecutarse con el agente integrado `Plan`, como exige el protocolo
  del repositorio;
- D2 debe continuar en el mismo chat, cambiando al agente integrado `Agent` y
  manteniendo `GPT-5.6 Terra`;
- D3 debe ejecutarse en el chat revisor independiente con `Agent` y el mismo
  modelo, pero sin permisos de edición.

No añadas `agent: agent` al frontmatter: forzaría Agent también al invocar D1 y
anularía la puerta obligatoria de Plan. Si `GPT-5.6 Terra` no aparece en el
selector del plan Copilot Pro o está restringido por la organización, detente y
comunica la limitación; no sustituyas el modelo silenciosamente.

## Contexto obligatorio del repositorio

Antes de analizar el escenario, lee por completo:

- `AGENTS.md`;
- `.github/copilot-instructions.md`;
- `.github/prompts/scenario-d-testing.prompt.md`;
- `.github/instructions/python.instructions.md`;
- `.github/instructions/tests.instructions.md`;
- `inventory_v4.py`;
- `pyproject.toml`;
- `tests/test_inventory_v4_console.py`;
- `tests/test_inventory_csv_filter.py`.

Resume una regla vinculante de cada archivo antes de continuar. Si falta un
archivo adjunto, detente y pide que se añada mediante **Add Context**.

Respeta especialmente estas reglas:

- `inventory_v4.py` es la línea base activa;
- `inventory.py`, `inventory_v2.py` e `inventory_v3.py` son históricos;
- `Product` mantiene las invariantes del dominio;
- `InventoryService` orquesta casos de uso y depende de
  `ProductRepository`;
- `InMemoryProductRepository` es infraestructura y se usa como colaborador real
  de las pruebas de servicio;
- una fase de testing no autoriza a corregir producción;
- las pruebas existentes no pueden modificarse, debilitarse ni sustituirse;
- no se puede tocar el archivo real `inventory_data.json`.

## Línea base de la carpeta de pruebas

La inspección previa a esta versión del prompt encontró:

- `tests/test_inventory_v4_console.py`, con pruebas de interfaz que usan
  colaboradores de prueba, `monkeypatch` y `capsys`;
- `tests/test_inventory_csv_filter.py`, correspondiente al escenario CSV;
- ningún `conftest.py`;
- ninguna prueba específica de `Product`, `ProductRepository`,
  `InMemoryProductRepository` o `InventoryService`.

Los colaboradores y fixtures usados por pruebas anteriores no autorizan su uso
en los tres archivos nuevos. Ambos archivos existentes permanecen congelados y
deben aprobar dentro de la suite completa. D1 debe volver a inventariar
`tests/` con herramientas de lectura y detenerse si aparece un archivo o cambio
no identificado por la tarjeta de lanzamiento.

## Protocolo obligatorio de lanzamiento

El archivo no se ejecuta automáticamente por existir en
`.github/prompts/`. Cada lanzamiento requiere los pasos siguientes.

### 1. Tarjeta de lanzamiento específica

Antes de cada lanzamiento, registra:

- rama esperada;
- estado esperado del árbol de trabajo;
- último commit base esperado.

Para la creación y revisión inicial de este prompt, el checkpoint comprobado
es:

```text
Rama: codex/scenario-d-testing
Estado de Git: limpio
Último commit:
523d6ed feat: refactor inventory v4 console for scenario C
```

Este checkpoint deja de ser válido después de modificar o confirmar el prompt.
Antes de ejecutar el escenario ya creado, genera una tarjeta nueva con el
commit que contenga la versión aprobada del prompt. No reutilices
`523d6ed` si ya no es el último commit o si el árbol no está limpio.

### 2. Verificación desde la terminal

En la terminal de VS Code, ejecuta:

```text
git branch --show-current
git status --short
git log -1 --oneline
```

Compara las tres salidas con la tarjeta de lanzamiento vigente. Detente si la
rama o el commit difieren, si el árbol debía estar limpio y no lo está, o si
aparece un cambio local que no haya sido identificado.

### 3. Selección del agente y contexto

Abre una sesión nueva de Copilot Chat para el escenario y selecciona el agente
integrado `Plan`, no `Agent`, para la fase D1. Confirma que el modelo activo es
`GPT-5.6 Terra` en Copilot Pro. Esa sesión será el chat de implementación
persistente después de la autorización y del cambio a `Agent`; no la reemplaces
en cada iteración. Si `Plan` o el modelo no están disponibles, detente y
comunica la limitación sin sustituirlos silenciosamente.

Mediante **Add Context**, adjunta explícitamente todos los archivos enumerados
en la sección «Contexto obligatorio del repositorio». Las instrucciones de
Python y tests son obligatorias durante D1 aunque todavía no se edite ningún
archivo `.py`.

### 4. Invocación manual

Invoca manualmente `/scenario-d-testing` y añade este mensaje, sustituyendo la
tarjeta por los valores vigentes y exactos:

```text
/scenario-d-testing

Ejecuta únicamente la fase D1 de análisis y preautorización.

Checkpoint de este lanzamiento:

- Rama: codex/scenario-d-testing
- Estado de Git: limpio
- Último commit: <pega aquí el hash y asunto vigentes de git log -1 --oneline>

Antes del análisis:

1. Confirma que has leído todos los archivos adjuntos, AGENTS.md y el prompt
   del escenario.
2. Resume una regla vinculante de cada archivo adjunto.
3. Verifica la rama, el estado de Git y el commit de esta tarjeta.
4. Activa venv y confirma Python 3.14.x y la versión instalada de pytest.
5. Revisa `pyproject.toml`, el inventario instalado y la integridad de
   dependencias sin instalar ni actualizar paquetes.
6. Trabaja exclusivamente con herramientas de lectura.
7. No crees, edites, formatees, muevas ni elimines archivos.

Entrega:

- introducción del escenario;
- inventario de la carpeta `tests/` y confirmación de pruebas previas intactas;
- tarjeta de las seis respuestas;
- inventario de contratos públicos;
- matriz de trazabilidad requisito-prueba;
- separación entre dominio, contrato de repositorio y servicio;
- delimitación entre dominio, repositorio, servicio y aplicación de consola;
- casos normales, límites, errores y conservación del estado;
- decisiones pendientes sobre bool, NaN, infinito, mensajes, orden, firma
  abstracta, abstracción, identidad y aliasing;
- registro congelado de contrato observable, intérprete y entorno;
- inventario y decisión sobre las dependencias actuales;
- lista única de aceptación;
- criterios automáticos de rechazo;
- comandos de verificación;
- alcance exacto propuesto para D2.

No implementes nada. Finaliza esperando mi autorización explícita para D2.
```

No cambies al agente `Agent` hasta que el programador haya revisado D1,
congelado el contrato y la lista única de aceptación, y autorizado
expresamente el alcance exacto de D2.

## Puerta obligatoria de entorno

Antes del análisis y de la implementación:

1. Activa el entorno virtual del proyecto:

   ```text
   source venv/bin/activate
   ```

2. Ejecuta:

   ```text
   command -v python
   python --version
   python -m pytest --version
   python -m ruff --version
   python -m pip list --format=freeze
   python -m pip check
   ```

3. Confirma Python 3.14.x.
4. Confirma que pytest pertenece a la serie 9.1 aprobada por el proyecto. La
   línea base inspeccionada al crear este prompt es pytest 9.1.1.
5. Confirma que Ruff pertenece al rango declarado por el proyecto y que
   `pip check` no informa dependencias rotas.
6. Contrasta el inventario instalado con `pyproject.toml` sin asumir que un
   rango abierto reproduce por sí solo las versiones exactas.
7. Si el intérprete, pytest, Ruff o la integridad de dependencias no coinciden,
   detente y comunica la discrepancia.

No instales, actualices ni reemplaces Python, pytest, Ruff, el entorno virtual
o ninguna dependencia para superar esta puerta.

## Congelación previa de contrato, entorno y aceptación

Antes de implementar D2 y antes de repetir cualquier revisión, debe existir un
único registro congelado y aprobado que contenga:

- rama y commit base exactos;
- estado conocido del árbol de trabajo;
- ruta del intérprete devuelta por `command -v python`;
- entorno activado mediante `source venv/bin/activate`;
- versión exacta de Python;
- versión exacta de pytest;
- versión exacta de Ruff;
- inventario exacto devuelto por `python -m pip list --format=freeze`;
- resultado de `python -m pip check`;
- rangos declarados en `pyproject.toml` y existencia o ausencia de un archivo
  de bloqueo;
- inventario del contrato observable de `Product` e `InventoryService`;
- decisiones aprobadas sobre `bool`, `NaN`, infinito, mensajes y orden;
- matriz de trazabilidad aprobada;
- una sola lista de aceptación normativa.

La línea base inspeccionada al crear este prompt es:

```text
Entorno virtual: venv
Python: 3.14.0
pytest: 9.1.1
Ruff: 0.16.0
Dependencias directas de desarrollo:
  pytest>=9.1,<10
  ruff>=0.15,<0.17
Dependencias transitivas instaladas de pytest:
  iniconfig==2.3.0
  packaging==26.2
  pluggy==1.6.0
  Pygments==2.20.0
Archivo de bloqueo: no existe
Integridad: pip check sin requisitos rotos
```

El implementador y el revisor deben ejecutar y registrar:

```text
source venv/bin/activate
command -v python
python --version
python -m pytest --version
python -m ruff --version
python -m pip list --format=freeze
python -m pip check
```

Si la ruta, el entorno, las versiones, el inventario o la integridad difieren
del registro aprobado, detén la implementación o revisión. No interpretes un
cambio de entorno como defecto del código y no actualices el entorno para
continuar.

La lista de aceptación de la sección «Lista única de aceptación congelada» es
la única fuente normativa. La matriz de trazabilidad y los catálogos de casos
explican y relacionan sus elementos, pero no constituyen listas alternativas.
No copies la aceptación en documentos o respuestas con diferencias sutiles.
Durante una iteración se puede hacer referencia a sus elementos, no
reescribirlos.

Cualquier cambio de contrato, entorno o aceptación invalida la congelación,
exige una nueva decisión del programador y obliga a actualizar el registro
antes de continuar.

## Documentación oficial permitida

Utiliza únicamente las fuentes oficiales siguientes. No uses blogs, respuestas
de foros, documentación de terceros ni rutas de Python distintas de `/3.14/`.

### Python 3.14

- [Definiciones de funciones — Python 3.14](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions)
- [Sentencia `try` — Python 3.14](https://docs.python.org/3.14/reference/compound_stmts.html#the-try-statement)
- [`collections.abc.Callable` — Python 3.14](https://docs.python.org/3.14/library/collections.abc.html#collections.abc.Callable)
- [`__main__` y punto de entrada — Python 3.14](https://docs.python.org/3.14/library/__main__.html)
- [`input()` — Python 3.14](https://docs.python.org/3.14/library/functions.html#input)
- [`print()` — Python 3.14](https://docs.python.org/3.14/library/functions.html#print)
- [Flujos estándar — Python 3.14](https://docs.python.org/3.14/library/sys.html#sys.stdin)
- [`sys.exit()` — Python 3.14](https://docs.python.org/3.14/library/sys.html#sys.exit)
- [Tutorial oficial de `argparse` — Python 3.14](https://docs.python.org/3.14/howto/argparse.html)

Estas fuentes permiten justificar:

- sintaxis de funciones, parámetros, retornos y anotaciones;
- ejecución del cuerpo de una función al invocarla;
- selección, manejo y propagación de excepciones;
- uso de `Callable` únicamente si un helper devuelve o recibe una función.
- separación entre la importación de un módulo y la ejecución de su punto de
  entrada mediante `if __name__ == "__main__"`;
- comportamiento básico de `input()`, `print()`, `stdin`, `stdout` y `stderr`;
- semántica general de `sys.exit()` para programas de consola;
- papel de `argparse` como analizador recomendado cuando una aplicación recibe
  argumentos de línea de comandos.

`Callable` es opcional. No crees factories, callbacks o helpers artificiales
solo para utilizarlo.

Estas fuentes describen mecanismos del lenguaje y la biblioteca estándar. No
definen qué es una capa backend, no establecen la arquitectura de Inventory y
no convierten consola en alcance del escenario D.

### pytest 9.1

- [Changelog de pytest 9.1.1](https://docs.pytest.org/en/stable/changelog.html#pytest-9-1-1)
- [Fixtures de pytest](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [Parametrización con pytest](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [`pytest.raises`](https://docs.pytest.org/en/stable/reference/reference.html#pytest-raises)
- [Buenas prácticas e identificación de tests](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
- [Códigos de salida de pytest](https://docs.pytest.org/en/stable/reference/exit-codes.html)

La documentación `stable` consultada al crear este prompt corresponde a pytest
9.1.1, confirmado por el changelog oficial y por el entorno local. Si `stable`
pasa a documentar una versión incompatible con la instalada, detente y solicita
una decisión; no adaptes el entorno ni uses documentación no verificada.

Estas fuentes permiten justificar:

- fixtures con alcance `function`, el alcance predeterminado, para obtener un
  repositorio y un servicio nuevos por prueba;
- `@pytest.mark.parametrize` con listas o tuplas concretas;
- `pytest.raises` como context manager para comprobar excepciones específicas;
- descubrimiento de archivos `test_*.py` y funciones `test_*`;
- ejecución desde el layout plano mediante `python -m pytest`;
- exigencia de código de salida `0` para una verificación satisfactoria.

No atribuyas a pytest:

- las invariantes de `Product`;
- la arquitectura o dirección de dependencias;
- los contratos de `InventoryService`;
- la decisión sobre `bool`, `NaN`, infinito, mensajes u orden;
- la obligación de usar `InMemoryProductRepository`;
- la conservación de estado que debe comprobar el proyecto.

Esas decisiones proceden del código, de las instrucciones locales y de la
autorización del programador.

### GitHub Copilot y prompt files

- [Formato de prompt files en VS Code](https://code.visualstudio.com/docs/agent-customization/prompt-files)
- [Modos Plan y Agent de GitHub Copilot](https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide?tool=vscode)
- [Modelos compatibles con GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models)

Estas fuentes permiten justificar:

- frontmatter con `name`, `description` y `model`;
- selección de `GPT-5.6 Terra`;
- uso de Plan para análisis y Agent para implementación;
- invocación manual del prompt mediante `/scenario-d-testing`.

No uses esas fuentes para justificar los contratos de Inventory ni las
expectativas de pytest.

## Delimitación de la aplicación de consola

La documentación oficial de Python distingue el punto de entrada y los flujos
de consola, pero la separación arquitectónica concreta procede de las
instrucciones del repositorio.

En `inventory_v4.py`:

- `main()` es el punto de composición que crea `JSONproductRepository` e
  `InventoryService`;
- el bloque `if __name__ == "__main__":` ejecuta `main()` solo al iniciar el
  módulo como programa, no al importarlo desde las pruebas;
- `show_menu`, `ask_*`, `handle_*` y `run_inventory_menu` pertenecen a la
  interfaz;
- `input()` obtiene interacción mediante la entrada estándar;
- `print()` produce la salida observable de la consola;
- los mensajes, reintentos, orden del menú y traducción de excepciones ya están
  congelados por `tests/test_inventory_v4_console.py`.

Por tanto, los tres archivos nuevos de D2:

- pueden importar `Product`, `ProductRepository`, `InventoryService`, sus
  excepciones e `InMemoryProductRepository` desde `inventory_v4` sin ejecutar
  `main()`;
- no deben llamar `main()`, `show_menu`, `ask_*`, `handle_*` ni
  `run_inventory_menu`;
- no deben sustituir `input()` ni interceptar `print()`;
- no deben usar `monkeypatch` ni `capsys`;
- no deben comprobar prompts, mensajes de consola, `stdout`, `stderr`, códigos
  de salida o argumentos de línea de comandos;
- no deben crear `JSONproductRepository` ni acceder a `inventory_data.json`;
- deben observar el estado exclusivamente mediante contratos públicos de
  `Product`, `ProductRepository`, `InMemoryProductRepository` e
  `InventoryService`.

La representación `str(product)` continúa dentro del alcance porque
`Product.__str__()` es un comportamiento público de la entidad. Esto no
autoriza a ejecutar la interfaz ni a duplicar las pruebas de consola.

`argparse` es la herramienta recomendada por la biblioteca estándar para
procesar argumentos de línea de comandos, pero Inventory utiliza actualmente
un menú interactivo basado en `input()`. Este escenario no autoriza a introducir
`argparse`, cambiar el punto de entrada, añadir códigos de salida ni convertir
el menú en una CLI basada en argumentos.

La documentación de consola se usa únicamente para reforzar el límite entre
interfaz y aplicación. No añade filas a la matriz de trazabilidad ni elementos
a la lista única de aceptación.

## Procedimientos pytest actualizados

### Aislamiento mediante fixtures

Las fixtures de repositorio y servicio deben tener alcance de función,
explícito o predeterminado. Cada prueba debe recibir un
`InMemoryProductRepository` nuevo. Las pruebas de servicio deben recibir además
un `InventoryService` nuevo conectado a ese repositorio.

No uses fixtures de alcance `class`, `module`, `package` o `session`, porque
compartirían objetos mutables y podrían volver las pruebas dependientes del
orden. No se necesita teardown: el repositorio solo vive en memoria y su
alcance termina con la prueba.

Mantén cada fixture dentro del archivo que la utiliza. No crees `conftest.py`
para tres archivos ni introduzcas estado autouse u oculto.

### Parametrización segura en pytest 9.1

Usa `@pytest.mark.parametrize` cuando varias entradas ejerciten el mismo
contrato. Los valores de `argvalues` deben ser listas o tuplas concretas.
pytest 9.1 depreca generadores, iteradores y otros iterables que no implementan
`Collection`.

Parametriza datos primitivos e inmutables siempre que sea posible. pytest pasa
los parámetros tal como están, sin copiarlos; por tanto, no compartas objetos
`Product`, listas o diccionarios mutables entre invocaciones parametrizadas.
Construye el objeto dentro de cada ejecución si luego será mutado.

Usa IDs descriptivos solo cuando aclaren el límite probado. No generes
parametrización dinámica, hooks, plugins ni opciones nuevas.

### Excepciones esperadas

Usa:

```text
with pytest.raises(ExpectedException):
    operation_that_must_fail()
```

La operación que debe lanzar debe ser la última instrucción dentro del bloque
`with`. Realiza fuera del bloque las aserciones sobre el estado posterior.

Espera tipos específicos como `TypeError`, `ValueError`,
`ProductAlreadyExistsError` o `ProductNotFoundError`. No uses
`pytest.raises(Exception)`, porque puede ocultar defectos no relacionados.

`pytest.raises` también acepta subclases del tipo esperado. Si el contrato
aprobado exige el tipo exacto, captura `exc_info` y comprueba
`exc_info.type is ExpectedException`.

Usa `match=` únicamente si el programador declara estable el mensaje. `match`
interpreta una expresión regular, no una igualdad literal. No congeles por
accidente puntuación o redacción incidental.

No uses `pytest.raises` para que una prueba continúe dentro del mismo bloque
después de la excepción; ese código no se ejecutaría. Las comprobaciones de
conservación de estado deben ir después del context manager.

### Descubrimiento y ejecución

Los archivos nuevos se llamarán:

- `tests/test_inventory_v4_domain.py`;
- `tests/test_inventory_v4_repository.py`;
- `tests/test_inventory_v4_service.py`.

Las pruebas se nombrarán `test_<comportamiento_observable>`. Ejecuta pytest
desde la raíz del repositorio con `python -m pytest`, de modo coherente con el
layout plano actual y sin modificar `PYTHONPATH`, el modo de importación ni
`pyproject.toml`.

Un resultado aceptado requiere código de salida `0`: tests recogidos y todos
aprobados. Los códigos distintos de cero, incluida la ausencia de tests
recogidos, son rechazo. En pytest 9.1, el código `5` indica que no se recogieron
tests y el código `6` que se superó el máximo de warnings configurado. No
instales plugins para alterar códigos de salida.

### Estructura y nombres de las pruebas

Separa el camino correcto de cada error esperado en funciones de prueba
distintas. No mezcles en un único test una operación válida y varias
excepciones para reducir el número de tests. La parametrización puede agrupar
entradas equivalentes solo cuando todas comprueban el mismo comportamiento y
pertenecen a la misma categoría:

- casos correctos con casos correctos;
- límites aceptados con límites aceptados;
- errores de tipo con errores de tipo;
- errores de valor con errores de valor;
- inexistentes con inexistentes cuando la regla y el estado protegido sean los
  mismos.

Usa nombres completos orientados a comportamiento, por ejemplo:

```text
test_product_strips_surrounding_whitespace_from_valid_name
test_product_rejects_negative_price_without_changing_previous_price
test_product_repository_cannot_be_instantiated_while_methods_are_abstract
test_in_memory_repository_rejects_duplicate_id_without_replacing_product
test_add_product_rejects_duplicate_id_without_replacing_existing_product
test_delete_product_raises_not_found_without_changing_inventory
```

Evita nombres como `test_product_1`, `test_error`, `test_validation` o nombres
que describan el helper usado en lugar del contrato comprobado.

Una prueba fallida es evidencia. No cambies su entrada, excepción esperada,
aserción, mensaje o estado posterior para adaptarla al comportamiento
defectuoso. Si la expectativa coincide con el contrato congelado, conserva la
prueba y registra el fallo.

## Alcance exacto de una futura fase D2

Una autorización posterior puede permitir exclusivamente:

- crear `tests/test_inventory_v4_domain.py`;
- crear `tests/test_inventory_v4_repository.py`;
- crear `tests/test_inventory_v4_service.py`.

No puede modificar, formatear, mover ni eliminar:

- `inventory_v4.py`;
- `Product`, `InventoryService` o sus excepciones;
- `ProductRepository`;
- `InMemoryProductRepository`;
- `JSONproductRepository`;
- las funciones de consola o `main()`;
- `inventory_data.json`;
- `pyproject.toml`;
- `AGENTS.md` ni archivos de instrucciones;
- este prompt;
- `tests/test_inventory_v4_console.py`;
- `tests/test_inventory_csv_filter.py`;
- ningún archivo histórico;
- el entorno virtual o archivos de dependencias.

No crees `conftest.py`, configuración de cobertura, snapshots, golden files,
helpers compartidos, datos persistentes ni archivos temporales.

## Dependencias y técnicas excluidas

No se introduce ninguna dependencia. pytest y Ruff ya pertenecen al grupo de
desarrollo del proyecto.

La revisión de dependencias realizada para este escenario establece:

- `pyproject.toml` no declara dependencias de producción;
- las únicas dependencias directas de desarrollo son `pytest>=9.1,<10` y
  `ruff>=0.15,<0.17`;
- pytest 9.1.1 requiere Python 3.10 o posterior, por lo que el Python 3.14.0
  congelado satisface su metadato instalado;
- sus dependencias transitivas obligatorias instaladas son `iniconfig`,
  `packaging`, `pluggy` y `Pygments`, y satisfacen sus rangos;
- Ruff 0.16.0 no incorpora dependencias de ejecución y el proyecto configura
  `target-version = "py314"`;
- `python -m pip check` no detecta requisitos rotos;
- no existe lockfile ni otro manifiesto de dependencias.

No es necesario modificar dependencias para D2. La ausencia de lockfile y los
rangos abiertos permiten que una reconstrucción futura resuelva otras versiones
compatibles; esta es una limitación de reproducibilidad, no un defecto de la
suite propuesta. No estreches rangos, no crees un lockfile y no modifiques
`pyproject.toml` en este escenario. Si el programador exige reproducibilidad
exacta en un entorno nuevo, detente: ese trabajo requiere análisis,
preautorización y alcance independientes.

Quedan expresamente excluidos:

- `unittest.mock` y librerías externas de mocks;
- fakes, stubs o repositorios de prueba alternativos;
- monkeypatch sobre métodos del repositorio o del servicio;
- acceso a red, JSON, CSV o sistema de archivos;
- herramientas o métricas nuevas de cobertura;
- Hypothesis u otros generadores;
- snapshots;
- `skip`, `skipif`, `xfail`, `importorskip` y expectativas condicionales;
- cambios en `pyproject.toml`;
- plugins o hooks de pytest;
- pruebas de atributos privados como `_products_by_id`;
- pruebas de implementación que sustituyan el contrato público.

## Inventario de contratos públicos

### Dominio — `Product`

El análisis D1 debe inventariar y clasificar:

- `Product(product_id, name, price, stock_quantity)`;
- propiedades de lectura `product_id`, `name`, `price` y `stock_quantity`;
- setters públicos de `name`, `price` y `stock_quantity`;
- `rename(new_name)`;
- `update_price(new_price)`;
- `update_stock(new_stock_quantity)`;
- `to_dict()`;
- `from_dict(data)`;
- `__str__()`.

Contratos actualmente observables que deben analizarse:

- `product_id` requiere `int` y valor mayor o igual que cero;
- `name` requiere `str`, elimina espacios exteriores y no puede quedar vacío;
- `price` requiere `int` o `float`, no puede ser negativo y se almacena como
  `float`;
- `stock_quantity` requiere `int` y no puede ser negativo;
- las mutaciones válidas actualizan solo el atributo solicitado;
- una validación fallida no debe reemplazar el valor válido anterior;
- `to_dict()` expone los cuatro campos;
- `from_dict()` reconstruye pasando de nuevo por el constructor;
- `__str__()` presenta ID, nombre, precio con dos decimales y stock.

No presupongas todavía una política para `bool`, `NaN` o infinito.

### Puerto de persistencia — `ProductRepository`

El análisis D1 debe inventariar:

- `ProductRepository` como clase base abstracta;
- `add(product) -> None`;
- `get_by_id(product_id) -> Product`;
- `list_all() -> list[Product]`;
- `update(product) -> None`;
- `delete(product_id) -> None`;
- `InMemoryProductRepository` como implementación concreta utilizada para
  validar el contrato.

El puerto abstracto no contiene una colección ejecutable. Por tanto, valida su
contrato público mediante `InMemoryProductRepository`, sin convertir
`JSONproductRepository` ni la persistencia en alcance. Analiza estos
comportamientos y lleva a D2 únicamente los aprobados:

- imposibilidad de instanciar el puerto sin implementar sus métodos abstractos;
- relación nominal entre `InMemoryProductRepository` y `ProductRepository`;
- listado inicial vacío;
- alta, recuperación, listado, actualización y eliminación;
- `ProductAlreadyExistsError` al añadir un identificador existente;
- `ProductNotFoundError` al recuperar, actualizar o eliminar un identificador
  inexistente;
- conservación de la colección y del producto original después de cada fallo.

Usa exclusivamente métodos y propiedades públicos. No inspecciones
`_products_by_id`. No pruebes tipos de entrada arbitrarios que el puerto no
declara y que pertenecen a las invariantes de `Product`.

El método abstracto `update` denomina actualmente `porduct` a su parámetro,
mientras la implementación usa `product`. Esta discrepancia observable debe
presentarse en D1 y no puede congelarse, corregirse ni ocultarse sin una
decisión explícita. Hasta entonces, invoca `update` de forma posicional.

### Aplicación — `InventoryService`

El análisis D1 debe inventariar:

- `InventoryService(repository)`;
- `add_product(product_id, name, price, stock_quantity) -> Product`;
- `list_products() -> list[Product]`;
- `find_product_by_id(product_id) -> Product`;
- `rename_product(product_id, new_name) -> Product`;
- `update_price(product_id, new_price) -> Product`;
- `update_stock(product_id, new_stock_quantity) -> Product`;
- `delete_product(product_id) -> None`.

Contratos que deben analizarse:

- el alta construye un `Product`, lo añade y devuelve un producto con los datos
  validados;
- el listado refleja la colección accesible mediante el repositorio;
- la búsqueda devuelve el producto solicitado o propaga
  `ProductNotFoundError`;
- renombrado, precio y stock recuperan el producto, aplican la regla de dominio,
  actualizan el repositorio y devuelven el resultado;
- el borrado exige que el producto exista y después lo elimina;
- un ID duplicado propaga `ProductAlreadyExistsError`;
- un dato de dominio inválido propaga `TypeError` o `ValueError`;
- un fallo esperado no debe crear, sustituir, mutar ni eliminar otros
  productos.

En las pruebas de servicio, `InMemoryProductRepository` sirve como colaborador
real. Comprueba el estado mediante métodos públicos de `InventoryService`, no
mediante `_products_by_id`. En las pruebas de repositorio, la implementación en
memoria es el objeto bajo prueba que permite verificar el contrato del puerto.

## Separación obligatoria entre dominio, repositorio y servicio

`tests/test_inventory_v4_domain.py` debe probar exclusivamente el
comportamiento público de `Product`. No debe crear servicios ni repositorios.

`tests/test_inventory_v4_repository.py` debe probar el contrato público de
`ProductRepository` mediante `InMemoryProductRepository`. Puede crear
`Product` válidos como datos de prueba, pero no debe repetir su matriz de
validación ni crear `InventoryService`.

`tests/test_inventory_v4_service.py` debe probar casos de uso completos de
`InventoryService` con `InMemoryProductRepository`. Puede usar `Product` para
preparar o observar datos, pero no debe repetir exhaustivamente todas las
validaciones del dominio.

La separación evita:

- probar dos veces la misma invariante en capas distintas;
- atribuir al puerto abstracto detalles privados de su implementación;
- convertir las pruebas de servicio en pruebas del diccionario interno;
- confundir un fallo del dominio con un fallo de orquestación;
- acoplar la suite a JSON, consola o persistencia real.

## Matriz mínima de trazabilidad requisito-prueba

Durante D1, completa y presenta una matriz al menos tan precisa como esta:

| Requisito | Capa | Evidencia mínima |
|---|---|---|
| Construcción válida | Dominio | propiedades normalizadas y tipos esperados |
| Valores cero | Dominio | ID, precio y stock aceptan el límite inferior |
| Nombre con espacios exteriores | Dominio | se conserva el contenido limpio |
| Tipo inválido por campo | Dominio | `TypeError` específico |
| Valor negativo o nombre vacío | Dominio | `ValueError` específico |
| Mutación válida | Dominio | cambia solo el atributo solicitado |
| Mutación inválida | Dominio | excepción y valor anterior intacto |
| Serialización | Dominio | `to_dict()` expone los cuatro campos |
| Reconstrucción | Dominio | `from_dict()` reaplica invariantes |
| Representación | Dominio | formato público actual de `str(product)` |
| Puerto abstracto | Repositorio | si se aprueba, no puede instanciarse incompleto |
| Implementación del puerto | Repositorio | si se aprueba, satisface la relación nominal |
| Listado inicial | Repositorio | colección pública vacía |
| Alta y recuperación | Repositorio | producto accesible por ID |
| Listado poblado | Repositorio | contiene todos los productos añadidos |
| Actualización existente | Repositorio | expone los nuevos datos |
| Eliminación existente | Repositorio | retorno `None` y consulta posterior falla |
| ID duplicado | Repositorio | excepción y producto original intacto |
| Consulta inexistente | Repositorio | excepción y colección intacta |
| Actualización inexistente | Repositorio | excepción y colección intacta |
| Eliminación inexistente | Repositorio | excepción y colección intacta |
| Alta | Servicio | producto añadido y devuelto |
| Listado vacío y poblado | Servicio | resultado accesible por API pública |
| Búsqueda existente | Servicio | datos del producto solicitado |
| Renombrado | Servicio | nombre actualizado y demás campos intactos |
| Cambio de precio | Servicio | precio actualizado y demás campos intactos |
| Cambio de stock | Servicio | stock actualizado y demás campos intactos |
| Eliminación | Servicio | retorno `None` y búsqueda posterior falla |
| ID duplicado | Servicio | excepción y producto anterior intacto |
| ID inexistente | Servicio | excepción y colección intacta |
| Dato inválido en alta | Servicio | excepción y ningún alta parcial |
| Dato inválido en actualización | Servicio | excepción y producto anterior intacto |

No consideres la matriz cerrada si falta un método público o un requisito
autorizado. No añadas filas de consola, JSON ni persistencia real.

## Casos normales, límites, errores y estado posterior

### Casos normales de `Product`

Incluye como mínimo:

- construcción con valores representativos;
- limpieza de espacios del nombre;
- conversión de precio entero a `float`;
- renombrado, actualización de precio y actualización de stock;
- `to_dict()` y `from_dict()` con datos válidos;
- representación textual.

### Límites de `Product`

Incluye:

- `product_id == 0`;
- `price == 0`;
- `stock_quantity == 0`;
- nombre mínimo no vacío después de `strip()`;
- valores inmediatamente inválidos: ID negativo, precio negativo, stock
  negativo, cadena vacía y cadena solo con espacios.

### Errores de `Product`

Parametriza con colecciones concretas:

- tipos no admitidos para ID;
- nombre no `str`;
- precio no numérico;
- stock no entero;
- valores negativos;
- nombre vacío.

Después de `rename`, `update_price`, `update_stock` o de un setter inválido,
comprueba fuera de `pytest.raises` que el estado anterior permanece intacto.

### Casos normales de `ProductRepository`

Mediante un `InMemoryProductRepository` nuevo por prueba, incluye:

- listado inicial vacío;
- alta y recuperación por ID;
- listado con varios productos;
- actualización de un producto existente;
- eliminación de un producto existente y retorno `None`.

Añade la no instanciabilidad del puerto y su relación nominal con la
implementación únicamente si D1 las congela como contrato.

### Límites de `ProductRepository`

Incluye productos válidos con identificador, precio y stock iguales a cero,
pero no repitas la validación exhaustiva del dominio. El orden del listado, la
identidad de los objetos y la independencia de la lista devuelta permanecen
pendientes hasta que el programador los declare contrato.

### Errores y conservación del estado del repositorio

Incluye:

- alta duplicada: conserva el producto original y el tamaño;
- recuperación inexistente: conserva la colección;
- actualización inexistente: conserva la colección;
- eliminación inexistente: conserva la colección.

Invoca `update` posicionalmente mientras no exista una decisión sobre el nombre
del parámetro abstracto. Captura la excepción específica y comprueba después el
estado mediante `get_by_id()` o `list_all()`.

### Casos normales de `InventoryService`

Incluye:

- listado inicial vacío;
- alta y retorno del producto;
- listado de productos existentes;
- búsqueda por ID;
- renombrado;
- actualización de precio;
- actualización de stock;
- eliminación y retorno `None`.

### Límites de `InventoryService`

Incluye un alta válida con valores cero y actualizaciones válidas a cero. No
dupliques toda la matriz de validación de `Product`; selecciona casos que
demuestren que el servicio delega correctamente en el dominio.

### Errores y conservación del estado del servicio

Incluye:

- alta con ID duplicado: conserva el producto original y el tamaño;
- alta con dato inválido: no añade ningún producto;
- búsqueda inexistente: no modifica la colección;
- renombrado inexistente: no modifica productos;
- precio inexistente: no modifica productos;
- stock inexistente: no modifica productos;
- eliminación inexistente: no elimina productos;
- nombre, precio o stock inválidos en un producto existente: propagan la
  excepción y conservan todos sus campos anteriores.

Captura la excepción con `pytest.raises` y verifica después el estado mediante
`list_products()` o `find_product_by_id()`.

## Decisiones que siguen perteneciendo al programador

D1 debe presentar explícitamente la evidencia actual y solicitar una decisión
antes de que D2 escriba una expectativa sobre cualquiera de estos puntos.

### `bool`

En Python, `bool` es compatible con comprobaciones basadas en `int`; el código
actual puede aceptar `True` y `False` para ID, precio o stock. Decidir si:

- se caracteriza esa aceptación como contrato actual; o
- se deja sin congelar hasta un escenario que autorice cambiar la regla.

No escribas una prueba que exija rechazo de `bool` si producción lo acepta.

### `NaN`

La comparación actual con cero no rechaza `float("nan")`. Decidir si se
caracteriza la aceptación o si se excluye de D2 hasta definir una regla de
negocio. No cambies producción.

### Infinito

El infinito positivo puede superar la validación actual; el negativo no.
Decidir si ese comportamiento se caracteriza o queda pendiente. No conviertas
«número» en «número finito» sin autorización.

### Mensajes de excepción

Decidir qué mensajes, fragmentos o puntuación forman parte del contrato. La
recomendación conservadora es comprobar tipos específicos y usar `match=` solo
para texto declarado estable. No confundas mensajes de infraestructura con
invariantes del dominio.

### Orden

`InMemoryProductRepository` conserva actualmente el orden de inserción debido a
su estructura interna, pero `ProductRepository.list_all()` no declara
formalmente un orden. Decidir si:

- el orden de inserción se congela como contrato; o
- las pruebas de repositorio y servicio comparan contenido sin convertir el
  orden en requisito.

No ordenes artificialmente producción ni dependas de `_products_by_id`.

### Firma abstracta de `update`

`ProductRepository.update` usa el nombre `porduct`, mientras
`InMemoryProductRepository.update` usa `product`. Decidir si:

- la discrepancia se registra sin congelarla y las pruebas llaman
  posicionalmente, opción recomendada para este escenario; o
- el nombre del parámetro se declara parte del contrato, lo que requeriría
  analizar por separado cualquier corrección de producción.

No escribas una prueba que exija corregir o conservar la errata sin decisión.

### Abstracción, identidad y aliasing

Decidir si la no instanciabilidad del ABC y la relación nominal de la
implementación forman parte del contrato arquitectónico. También decidir si la
identidad de los `Product` devueltos o la independencia de la lista de
`list_all()` son observables normativos. La recomendación es congelar ABC y
herencia, pero no identidad ni aliasing mientras el puerto no los declare.

Si el programador no decide un punto, D2 debe excluir únicamente esa
expectativa y registrar la cobertura pendiente. No debe inventar una respuesta.

## Tarjeta de preautorización de seis respuestas

Estas respuestas constituyen la base teórica aprobada del escenario. D1 debe
contrastarlas con el código vigente y comunicar cualquier discrepancia, pero no
reformularlas ni sustituirlas por otra tarjeta sin una decisión del
programador.

### 1. ¿Qué capa se modifica?

Exclusivamente la capa de pruebas, creando:

- `tests/test_inventory_v4_domain.py`;
- `tests/test_inventory_v4_repository.py`;
- `tests/test_inventory_v4_service.py`.

### 2. ¿Por qué es la capa correcta?

Porque `Product`, `ProductRepository`, `InMemoryProductRepository` e
`InventoryService` ya están implementados. El objetivo es validar sus contratos
públicos y reglas actuales, no cambiar dominio, aplicación, persistencia o
consola.

### 3. ¿Qué dependencia se introduce?

Ninguna. Se utiliza pytest 9.1.1, ya instalado, junto con:

- `pytest.mark.parametrize`;
- `pytest.raises`;
- fixtures sencillas cuando reduzcan preparación repetida;
- `InMemoryProductRepository` como implementación del contrato y colaborador
  del servicio.

`monkeypatch` y `capsys` siguen disponibles como parte de pytest, pero no son
necesarios ni están autorizados para las pruebas de dominio, repositorio y
servicio. No se añade una librería de mocks ni una herramienta de cobertura.

### 4. ¿Qué contrato público u observable se preserva?

Las firmas públicas de `Product`, `ProductRepository`,
`InMemoryProductRepository` e `InventoryService`; los tipos de excepciones
actuales; los valores devueltos; los cambios de estado; y el comportamiento ya
congelado de consola, JSON y pruebas anteriores.

### 5. ¿Qué reglas de negocio se protegen?

Principalmente:

- identificador entero y no negativo;
- nombre de texto, recortado y no vacío;
- precio numérico y no negativo;
- stock entero y no negativo;
- unicidad del identificador;
- cumplimiento de alta, recuperación, listado, actualización y eliminación del
  contrato de repositorio;
- error al buscar, actualizar o eliminar productos inexistentes;
- validación de las modificaciones antes de alterar el estado;
- coordinación correcta de los casos de uso por `InventoryService`.

### 6. ¿Qué pruebas demuestran el resultado?

Una suite separada por responsabilidad:

| Área | Casos normales | Límites | Errores y excepciones |
|---|---|---|---|
| `Product` | Construcción, modificación, serialización y representación | Cero, nombre con espacios y precio entero normalizado | Tipos incorrectos, negativos, nombre vacío y estado preservado tras modificación inválida |
| `ProductRepository` mediante `InMemoryProductRepository` | Abstracción, alta, recuperación, listado, actualización y eliminación | Colección vacía y productos con valores cero | Duplicados, inexistentes y estado preservado tras el fallo |
| `InventoryService` | Añadir, listar, encontrar, renombrar, cambiar precio o stock y eliminar | Inventario vacío, valores cero y secuencias con varios productos | Duplicados, producto inexistente, datos de dominio inválidos y propagación de excepciones |

D1 debe añadir nombres de pruebas propuestos y vincular cada respuesta a
evidencia sin crear una segunda lista de aceptación.

## Lista única de aceptación congelada para D2 y revisión

Esta es la única lista de aceptación normativa del escenario. D1 debe
completarla con los nombres de tests y decisiones aprobados sin crear una
segunda lista. Una D2 autorizada y su revisión independiente se aceptan
únicamente si:

- existen exactamente los tres archivos nuevos permitidos;
- se separan pruebas de dominio, repositorio y servicio;
- cada prueba es determinista e independiente;
- las fixtures de repositorio y servicio crean estado nuevo por prueba;
- el contrato de `ProductRepository` se valida mediante
  `InMemoryProductRepository`;
- el servicio usa `InMemoryProductRepository`;
- no existen mocks, fakes ni monkeypatch;
- la parametrización usa listas o tuplas, no generadores;
- las excepciones se comprueban con tipos específicos;
- las comprobaciones posteriores a una excepción están fuera de
  `pytest.raises`;
- los fallos dejan intacto el estado exigido;
- no se accede a atributos privados;
- no se toca JSON, CSV, consola, red ni sistema de archivos;
- ningún test nuevo llama al punto de entrada ni a funciones de interfaz;
- ningún test nuevo usa `monkeypatch`, `capsys`, `input()` o aserciones sobre
  flujos estándar;
- `tests/test_inventory_v4_console.py` permanece sin cambios y continúa
  aprobando dentro de la suite completa;
- no hay skips, `xfail` ni cobertura nueva;
- las decisiones numéricas, de mensajes, orden, firma abstracta, abstracción,
  identidad y aliasing coinciden con la autorización;
- la selección nueva y la suite completa terminan con código de salida `0`;
- Ruff aprueba los tres archivos;
- el diff solo contiene los archivos autorizados.

Una prueba que revele un defecto real debe quedar como evidencia. No modifiques
producción ni cambies la expectativa para obtener verde. Informa del fallo y
solicita una autorización separada para cualquier corrección.

## Flujo obligatorio de trabajo

### Fase D1 — Análisis y preautorización

1. Supera el protocolo de lanzamiento y la puerta de entorno.
2. Lee y resume todos los archivos adjuntos.
3. Usa exclusivamente herramientas de lectura.
4. Inspecciona los contratos públicos y las pruebas existentes.
5. Entrega:

   - introducción;
   - checkpoint y entorno;
   - inventario de la carpeta `tests/`;
   - tarjeta de seis respuestas;
   - inventario de contratos;
   - separación entre dominio, repositorio y servicio;
   - delimitación de la aplicación de consola fuera del alcance;
   - matriz de trazabilidad;
   - catálogo de casos normales, límites y errores;
   - estrategia de conservación de estado;
   - decisiones pendientes;
   - registro congelado de contrato, intérprete y entorno;
   - lista única de aceptación propuesta;
   - criterios de rechazo;
   - comandos de verificación;
   - alcance exacto propuesto para D2.

6. No crees, edites, formatees, muevas ni elimines archivos.
7. No ejecutes pruebas si hacerlo puede crear cachés durante la fase declarada
   de solo lectura. La comprobación de versiones sí está permitida.
8. Termina exactamente con:

   ```text
   Esperando autorización explícita para la fase D2.
   ```

Después, detente.

### Puerta de autorización

Continúa únicamente si el programador autoriza expresamente:

- crear `tests/test_inventory_v4_domain.py`;
- crear `tests/test_inventory_v4_repository.py`;
- crear `tests/test_inventory_v4_service.py`;
- el registro congelado de contrato, intérprete y entorno;
- la lista única de aceptación;
- la matriz concreta de casos;
- las decisiones adoptadas sobre `bool`, `NaN`, infinito, mensajes, orden,
  firma abstracta, abstracción, identidad y aliasing.

Una nueva autorización es obligatoria si aparece otro archivo, capa,
dependencia, firma, excepción, mensaje estable, regla, expectativa o
comportamiento observable.

### Fase D2 — Implementación autorizada

1. Continúa en el mismo chat de implementación usado para D1 y cambia al agente
   `Agent` solo después de la autorización. Mantén seleccionado
   `GPT-5.6 Terra` en Copilot Pro.
2. Revalida el registro congelado: rama, commit, entorno virtual, ruta del
   intérprete, Python y pytest.
3. Repite la lista única de aceptación solo por referencia; no la reescribas ni
   abras una lista alternativa.
4. Crea únicamente los tres archivos autorizados.
5. Escribe primero las pruebas de `Product`.
6. Mantén separados los casos correctos y los errores esperados.
7. Nombra cada test según el comportamiento que comprueba.
8. Ejecuta la selección de dominio.
9. Escribe las pruebas de `ProductRepository` contra
   `InMemoryProductRepository`.
10. Ejecuta la selección de repositorio.
11. Escribe las pruebas de `InventoryService` usando fixtures de función e
    `InMemoryProductRepository`.
12. Ejecuta la selección de servicio.
13. Ejecuta conjuntamente los tres archivos nuevos.
14. Ejecuta la suite completa.
15. Ejecuta Ruff sobre los archivos nuevos.
16. Inspecciona markers prohibidos, diff y estado de Git.
17. Si una prueba falla porque producción no satisface una expectativa
    autorizada, detente y presenta la evidencia. No edites producción.
18. No modifiques una prueba para ocultar o reclasificar el fallo.
19. No hagas staging, commit ni push sin otra autorización explícita.

### Fase D3 — Revisión independiente persistente

La revisión independiente requiere una persona o agente revisor distinto del
implementador y un chat revisor separado. El implementador no puede
autorrevisarse cambiando de rol dentro de su propio chat.

Abre el chat revisor una sola vez después de que D2 entregue una implementación
completa para revisar. Selecciona `Agent` con `GPT-5.6 Terra` en Copilot Pro,
limita su actuación a lectura y verificación, y adjunta:

- todos los archivos del «Contexto obligatorio del repositorio»;
- `tests/test_inventory_v4_domain.py`;
- `tests/test_inventory_v4_repository.py`;
- `tests/test_inventory_v4_service.py`;
- el registro congelado;
- la lista única de aceptación aprobada;
- el informe de implementación con los comandos y resultados.

El revisor trabaja sin editar archivos y debe:

1. confirmar que es distinto del implementador;
2. revalidar rama, commit o diff esperado, árbol de trabajo, `venv`, ruta del
   intérprete, Python y pytest;
3. comparar las pruebas con el contrato y la lista única congelados;
4. comprobar separación entre casos correctos y errores esperados;
5. comprobar nombres orientados al comportamiento;
6. ejecutar los comandos de verificación;
7. revisar el diff y detectar accesos privados, dependencias, markers o cambios
   fuera de alcance;
8. emitir un único informe consolidado con todos los hallazgos y su evidencia;
9. aprobar o rechazar sin corregir código ni pruebas.

Si el revisor rechaza:

1. conserva el mismo chat revisor y su contexto;
2. devuelve el informe consolidado al chat de implementación original;
3. corrige únicamente en el chat de implementación;
4. no cambies una prueba que refleje el contrato congelado para obtener verde;
5. devuelve el nuevo diff y resultados al mismo chat revisor;
6. repite allí la revisión completa contra la misma aceptación.

No abras un chat revisor nuevo por cada corrección. Solo se permite otro chat:

- para una auditoría final limpia después de que la revisión persistente haya
  aprobado; o
- cuando el contexto del revisor anterior haya quedado objetivamente
  invalidado por un cambio autorizado de contrato, entorno, baseline o alcance.

En caso de invalidación, registra la causa, vuelve a congelar contrato, entorno
y aceptación, y proporciona el registro completo al nuevo revisor.

## Criterios automáticos de rechazo

Detén el trabajo y considera D1 o D2 rechazada si:

- la rama, limpieza o commit no coinciden con la tarjeta vigente;
- el agente `Plan` no está disponible para D1;
- falta un archivo obligatorio de **Add Context**;
- se implementa o repite una revisión sin contrato, entorno y aceptación
  congelados;
- existen dos listas de aceptación o versiones divergentes de la misma;
- cambia la ruta del intérprete, el entorno virtual o una versión congelada sin
  decisión del programador;
- Python no es 3.14.x;
- pytest no pertenece a la versión aprobada;
- Ruff no pertenece al rango aprobado;
- `python -m pip check` informa requisitos rotos;
- el inventario instalado difiere del registro congelado;
- se consulta documentación no oficial o incompatible;
- se modifica un archivo fuera de los tres tests permitidos;
- se modifica producción, configuración, datos o pruebas anteriores;
- se crea `conftest.py` u otro archivo auxiliar;
- se añade o actualiza una dependencia;
- se usa JSON, CSV, consola, red o archivos reales;
- un test nuevo llama `main()`, `show_menu`, una función `ask_*`, `handle_*` o
  `run_inventory_menu`;
- un test nuevo usa `monkeypatch`, `capsys`, sustituye `input()` o captura
  `stdout` o `stderr`;
- se introduce `argparse`, se modifica el punto de entrada o se añade un código
  de salida;
- se usa un repositorio distinto de `InMemoryProductRepository`;
- el contrato de `ProductRepository` se prueba solo indirectamente mediante el
  servicio;
- una prueba llama `ProductRepository.update` por palabra clave sin una
  decisión aprobada sobre `porduct`;
- se crea un mock, fake, stub o monkeypatch;
- se inspecciona `_products_by_id` u otro detalle privado;
- se usa un generador o iterador como `argvalues`;
- se comparte un `Product` mutable entre casos parametrizados;
- un mismo test mezcla un caso correcto y un error esperado;
- un test no está nombrado según el comportamiento público que comprueba;
- se usa `pytest.raises(Exception)` o una excepción demasiado amplia;
- una aserción posterior al fallo se coloca dentro del bloque
  `pytest.raises`;
- se usa `match=` para un mensaje no aprobado;
- se congela sin decisión `bool`, `NaN`, infinito, orden, firma abstracta,
  abstracción, identidad o aliasing;
- aparece `skip`, `skipif`, `xfail` o `importorskip`;
- se añade cobertura, plugin, hook o configuración pytest;
- no se recogen pruebas;
- pytest devuelve un código distinto de `0`;
- Ruff falla;
- se modifica una expectativa para ocultar un defecto;
- el implementador actúa también como revisor independiente;
- el revisor edita código o pruebas en vez de informar;
- se abre un chat revisor nuevo para cada iteración sin invalidación objetiva;
- tras un rechazo no se consolidan los hallazgos o no se reutiliza el mismo
  chat revisor;
- se intenta arreglar producción sin una autorización nueva;
- se incluye trabajo ajeno en staging, commit o push.

Ante un rechazo, informa la condición, el comando y la salida exacta. No
expandas el alcance ni instales herramientas.

## Comandos de verificación de D2 y D3

Con `venv` activado y desde la raíz, ejecuta en este orden:

```text
command -v python
python --version
python -m pytest --version
python -m ruff --version
python -m pip list --format=freeze
python -m pip check
python -m pytest --collect-only -q tests/test_inventory_v4_domain.py tests/test_inventory_v4_repository.py tests/test_inventory_v4_service.py
python -m pytest tests/test_inventory_v4_domain.py
python -m pytest tests/test_inventory_v4_repository.py
python -m pytest tests/test_inventory_v4_service.py
python -m pytest tests/test_inventory_v4_domain.py tests/test_inventory_v4_repository.py tests/test_inventory_v4_service.py
python -m pytest
python -m ruff check tests/test_inventory_v4_domain.py tests/test_inventory_v4_repository.py tests/test_inventory_v4_service.py
rg -n "pytest\\.(skip|xfail|importorskip)|pytest\\.mark\\.(skip|skipif|xfail)" tests/test_inventory_v4_domain.py tests/test_inventory_v4_repository.py tests/test_inventory_v4_service.py
git diff --check
git branch --show-current
git log -1 --oneline
git status --short
```

Para el comando `rg`, la salida esperada es vacía; su código `1` significa que
no encontró markers prohibidos y no constituye por sí solo un fallo de la
suite.

Registra:

- cantidad de tests recogidos;
- aprobados y fallidos por selección;
- resumen de la suite completa;
- ausencia de skips y `xfail`;
- resultado de Ruff;
- ruta del intérprete y versiones comparadas con el registro congelado;
- archivos mostrados por Git;
- cualquier verificación no ejecutada y su motivo.

## Informe final de implementación y revisión

El implementador informa:

- archivos creados y capas cubiertas;
- dependencia introducida, indicando expresamente «ninguna»;
- contratos y reglas protegidos;
- decisiones aplicadas sobre `bool`, `NaN`, infinito, mensajes, orden, firma
  abstracta, abstracción, identidad y aliasing;
- fixtures y parametrización utilizadas;
- evidencia de conservación de estado;
- comandos exactos, códigos de salida y conteos;
- defectos descubiertos sin corregir;
- riesgos y decisiones que siguen perteneciendo al programador.

El revisor independiente añade:

- identidad de rol distinta del implementador;
- chat revisor reutilizado o causa documentada de invalidación;
- aceptación usada, sin crear otra lista;
- hallazgos consolidados y estado de cada uno;
- comandos repetidos y resultados exactos;
- veredicto de aprobación o rechazo;
- si se realizó una auditoría final limpia.

No declares completado el escenario con pruebas fallidas, checks omitidos sin
explicación, archivos fuera de alcance o estado Git no revisado.
