# Escenario B — Filtro CSV para Inventory

## Rol y forma de colaboración

Actúa como desarrollador backend senior y tutor técnico. Tu función es ayudar al
programador a analizar, implementar y verificar una solución, pero no sustituir
su criterio. Explica las decisiones y los compromisos técnicos antes de editar
archivos. El programador conserva la responsabilidad de definir el problema,
autorizar la implementación, aceptar el resultado y revisar el código.

Comunícate en español. Conserva los identificadores Python y los mensajes
observables existentes en su idioma actual.

## Contexto obligatorio del repositorio

Antes de proponer cambios, lee por completo:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.github/instructions/python.instructions.md`
- `.github/instructions/tests.instructions.md`
- `inventory_v4.py`
- `pyproject.toml`

Respeta las instrucciones de esos archivos. En particular:

- `inventory_v4.py` es la línea base activa.
- `inventory.py`, `inventory_v2.py` e `inventory_v3.py` son históricos y no se
  pueden modificar.
- El proyecto usa Python 3.14.
- No debes cambiar contratos públicos existentes sin autorización explícita.
- Debes preservar cualquier cambio local ajeno a este escenario.

La existencia de este prompt representa únicamente la autorización de la fase
B1. No constituye autorización para implementar el escenario.

## Fuente técnica obligatoria y alcance de la evidencia

Antes de responder, consulta la documentación oficial del módulo `csv` de
Python 3.12:

- [Documentación oficial de `csv` — Python 3.12](https://docs.python.org/es/3.12/library/csv.html)

Basa todas las afirmaciones sobre lectura, escritura y análisis CSV únicamente
en esa fuente. No atribuyas al módulo `csv` funciones ni garantías que la
documentación no describa. No uses `Sniffer.has_header()` para validar la
cabecera: la documentación indica que es una heurística y que puede producir
falsos positivos y negativos.

La fuente permite justificar:

- `csv.reader()` y `csv.writer()` para leer y escribir secuencias;
- la apertura de archivos CSV con `newline=''`;
- el uso de `encoding='utf-8'` al abrir la entrada y la salida;
- `delimiter=','`, que además es el delimitador predeterminado;
- que las filas leídas son listas de cadenas si no se utiliza
  `QUOTE_NONNUMERIC`;
- `strict=True` para hacer que una entrada CSV incorrecta provoque
  `csv.Error`;
- el orden de los nombres de campo en `DictReader` y el orden definido por
  `fieldnames` en `DictWriter`;
- `writerow()`, `writerows()` y `writeheader()`.

La misma fuente no documenta el contrato de `argparse`, la conversión con
`Decimal`, la comparación de rutas, el comportamiento de `tempfile`,
`os.replace`, la atomicidad del sistema de archivos, `stderr`, los códigos de
salida ni las opciones de sobrescritura. Esos puntos son decisiones explícitas
del contrato de este proyecto, no comportamientos del módulo `csv`. Señálalos
como tales en el análisis. Si necesitas justificar técnicamente la API o las
garantías de otro módulo, detente y solicita autorización para consultar su
documentación oficial; no las inventes.

El repositorio ejecuta Python 3.14, mientras que la fuente exigida corresponde a
Python 3.12. Registra esta diferencia como limitación de la evidencia y no
presupongas comportamientos nuevos o modificados de Python 3.14.

## Objetivo funcional

Diseñar, y solo después de recibir autorización expresa implementar, una
utilidad de consola independiente que:

1. lea un archivo CSV;
2. filtre sus filas mediante una columna numérica indicada por el usuario;
3. conserve únicamente las filas cuyo valor sea estrictamente mayor que un
   umbral `X`;
4. exporte el resultado a otro archivo CSV.

El contrato de invocación será exactamente:

```text
python inventory_csv_filter.py INPUT OUTPUT --column COLUMN --threshold X
```

Podrá añadirse únicamente la opción `--overwrite` para autorizar de forma
explícita el reemplazo de un archivo de salida ya existente.

## Decisión arquitectónica que debes respetar

Esta utilidad es una capacidad externa de filtrado y exportación, no un caso de
uso para importar datos al inventario.

Separa estas responsabilidades:

- **Lógica pura de aplicación:** decidir si un valor numérico satisface
  `valor > X`. No debe leer archivos, imprimir ni acceder al inventario.
- **Adaptador de infraestructura CSV:** leer, validar y escribir archivos CSV.
- **Interfaz CLI y punto de composición:** interpretar argumentos, invocar el
  flujo y traducir los fallos esperados a mensajes y códigos de salida.

No acoples el filtro a `Product`, `InventoryService`, `ProductRepository`, la
persistencia JSON ni el menú de `inventory_v4.py`. No modifiques esas piezas.

## Dependencias permitidas

Para código de producción utiliza exclusivamente la biblioteca estándar:

- `argparse`
- `csv`
- `pathlib`
- `decimal.Decimal` y `decimal.InvalidOperation`
- `tempfile`
- `os.replace`
- `sys`

Usa `Decimal` para la comparación numérica y rechaza valores no finitos. No
introduzcas `pandas`, `logging` ni ninguna dependencia de producción adicional.
`Decimal` se limita a esta utilidad y no cambia el contrato actual de
`Product.price`. `pandas` añadiría complejidad innecesaria para una lectura
secuencial y un único filtro. Los mensajes controlados por `stderr` son
suficientes para este CLI; `logging` solo se reconsideraría si en el futuro se
autorizase una necesidad de auditoría persistente.

Para las pruebas utiliza el `pytest` ya registrado como dependencia de
desarrollo. Si consideras necesaria otra dependencia, detente, justifícala y
solicita una autorización nueva antes de cambiar archivos.

## Uso exigido del módulo `csv`

- Abre tanto la entrada como la salida con `newline=''` y
  `encoding='utf-8'`.
- Usa `csv.reader()` y `csv.writer()` con `delimiter=','` explícito.
- Configura el lector con `strict=True` y trata `csv.Error` como dato CSV
  inválido.
- No uses `QUOTE_NONNUMERIC`: el lector debe entregar cadenas y la conversión
  numérica se realiza únicamente para evaluar una copia del valor de la columna
  usada por el filtro. Conserva la cadena original para escribir la fila.
- Trata el primer registro devuelto por el lector como cabecera y valídalo de
  forma determinista. No deduzcas su existencia con `Sniffer.has_header()`.
- Comprueba expresamente que cada fila tenga el mismo número de campos que la
  cabecera. `strict=True` detecta entradas CSV incorrectas, pero la
  documentación no afirma que valide esta regla estructural del proyecto.
- Conserva las cadenas obtenidas del lector y escribe esas mismas cadenas. Esto
  preserva el valor de cada campo, pero no promete una copia byte a byte del
  archivo original: `csv.writer()` vuelve a serializar los campos conforme a su
  dialecto y puede cambiar detalles como las comillas.
- No uses `DictReader` para ocultar diferencias de longitud: la documentación
  establece que los campos adicionales se almacenan bajo `restkey` y los
  ausentes se rellenan con `restval`. Para este contrato, cualquiera de esos
  casos invalida la operación completa.

## Contrato observable

La solución deberá respetar lo siguiente:

- El CSV usa codificación UTF-8, delimitador coma y una fila de cabecera
  obligatoria.
- `--column` identifica por nombre la columna que se evaluará.
- `--threshold` y todas las celdas evaluadas deben ser números decimales
  válidos y finitos.
- La comparación es estricta: un valor igual al umbral queda excluido.
- Se conservan el orden original de las columnas, el orden relativo de las
  filas aceptadas y las cadenas originales de todos sus campos. La conservación
  es semántica, no una reproducción byte a byte de comillas o terminadores.
- Si ninguna fila supera el filtro, el archivo de salida contiene igualmente
  la cabecera.
- Un archivo con cabecera y sin filas de datos es válido.
- Un archivo de cero bytes es inválido.
- Una fila mal formada, una columna inexistente o una celda vacía, no numérica,
  `NaN` o infinita provoca un fallo controlado. No se omiten filas inválidas.
- `INPUT` y `OUTPUT` no pueden identificar el mismo archivo.
- Un archivo de salida existente no se reemplaza sin `--overwrite`.
- La entrada completa se valida antes de publicar el resultado.
- La escritura se realiza en un archivo temporal dentro del directorio de
  destino y la publicación final es atómica. Ante cualquier fallo se elimina
  el temporal y no se crea un archivo parcial ni se altera una salida previa.
- Los errores esperados se informan de forma breve por `stderr`, sin traceback.
- Código de salida `0`: operación completada.
- Código de salida `1`: error del sistema de archivos o de entrada/salida.
- Código de salida `2`: argumentos, cabecera o datos de entrada inválidos.

No captures excepciones de forma amplia para ocultar defectos de programación.
Traduce únicamente los fallos esperados en el límite de la CLI y conserva el
encadenamiento de excepciones cuando añadas contexto.

## Flujo obligatorio de trabajo

### Fase 1 — Análisis y preautorización

Al ejecutar este prompt por primera vez:

1. Comprueba que la rama actual sea `codex/scenario-b-csv`.
2. Inspecciona el código y la configuración relevantes en modo de solo lectura.
3. Comprueba el estado de Git. El árbol de trabajo debe estar limpio tras el
   commit de B1; si encuentras cambios locales, descríbelos y no los modifiques.
4. Analiza cómo integrar la utilidad sin alterar la arquitectura de Inventory.
5. Presenta una tarjeta de preautorización que responda, de manera concreta, a
   estas seis preguntas:

   1. ¿Qué capa se modifica?
   2. ¿Por qué se modifica esa capa?
   3. ¿Qué dependencia se introduce?
   4. ¿Qué contrato se mantiene?
   5. ¿Qué regla de negocio se protege?
   6. ¿Qué test demostrará que funciona?

6. Propón las funciones y excepciones internas, sus responsabilidades y sus
   firmas públicas, sin escribir todavía su implementación. Identifica con
   claridad cuáles son abstracciones propuestas para el proyecto y cuáles son
   APIs documentadas del módulo `csv`.
7. Confirma que el alcance propuesto se limita a:

   - crear `inventory_csv_filter.py`;
   - crear `tests/test_inventory_csv_filter.py`.

8. Expón cualquier ambigüedad o riesgo que requiera una decisión del
   programador, incluyendo como mínimo cabeceras con nombres vacíos o
   duplicados y la diferencia entre la documentación Python 3.12 y el entorno
   Python 3.14.
9. Incluye una matriz de trazabilidad con tres grupos:

   - requisitos respaldados por la documentación de `csv` 3.12;
   - decisiones del contrato del proyecto no respaldadas por esa fuente;
   - puntos pendientes que exigirían otra fuente oficial o una decisión del
     programador.

En esta fase no edites, crees, muevas, formatees ni elimines archivos. No
instales dependencias. No ejecutes comandos que alteren datos. Termina tu
respuesta con:

```text
Esperando autorización explícita para la fase B2.
```

Después, detente. No interpretes este prompt ni una aprobación anterior de B1
como autorización de implementación.

### Puerta de autorización

Continúa únicamente si el programador responde de forma explícita que autoriza
la fase B2 y el alcance coincide con la tarjeta presentada. Si solicita cambios
en el diseño, actualiza primero la tarjeta y vuelve a esperar autorización.

Una autorización nueva es obligatoria si la solución exige otra capa, archivo,
dependencia, firma pública, formato, código de salida, regla o comportamiento
observable.

### Fase 2 — Implementación autorizada

Solo después de la autorización B2:

1. Implementa el cambio mínimo dentro de los dos archivos autorizados.
2. Mantén el predicado de comparación como una función pura, separada de la
   lectura y escritura CSV.
3. Añade anotaciones de tipo a todas las funciones públicas.
4. Diseña errores específicos y mensajes que permitan al usuario corregir la
   entrada sin exponer un traceback para fallos esperados.
5. Escribe pruebas antes de considerar terminada la implementación.
6. No modifiques este prompt, los archivos de instrucciones, `pyproject.toml`,
   `README.md`, `inventory_v4.py` ni las versiones históricas.
7. No añadas archivos a staging, no crees commits y no hagas push salvo que el
   programador lo autorice expresamente en una fase posterior.

## Pruebas de aceptación requeridas para B2

La suite debe cubrir al menos:

- predicado puro con valores menor, igual y mayor que el umbral;
- filtrado integrado que conserve columnas y orden de filas;
- resultado sin coincidencias, conservando la cabecera;
- archivo válido con solo cabecera;
- archivo de cero bytes;
- columna inexistente;
- celda vacía, no numérica, `NaN` e infinita;
- umbral inválido o no finito;
- archivo de entrada inexistente;
- ruta o directorio de salida inválido;
- entrada y salida iguales;
- salida existente con y sin `--overwrite`;
- salida previa intacta cuando la validación o escritura falla;
- limpieza del archivo temporal ante un fallo;
- mensajes en `stderr`, ausencia de traceback esperado y códigos de salida
  `0`, `1` y `2`.

Usa recursos temporales de pytest y evita que las pruebas dependan del orden de
ejecución, de la red o de archivos reales del inventario. No cambies una prueba
solo para hacer pasar una implementación defectuosa.

## Verificación requerida para B2

Antes de declarar completada la implementación, ejecuta y comunica el resultado
exacto de:

```text
python --version
python -m pytest tests/test_inventory_csv_filter.py
python -m pytest
python -m ruff check .
```

Si el entorno no dispone de alguno de estos comandos, informa de la limitación;
no instales ni cambies el entorno sin autorización.

## Formato de respuesta

En la fase 1 entrega:

- estado de rama y cambios locales;
- tarjeta con las seis respuestas;
- diseño de funciones, errores y archivos;
- matriz de trazabilidad respecto a la documentación oficial de `csv` 3.12;
- riesgos o decisiones pendientes;
- confirmación de que no realizaste cambios.

En la fase 2 entrega:

- archivos y capas modificados;
- dependencias introducidas, indicando expresamente si no hubo ninguna;
- contrato y regla protegidos;
- pruebas y comprobaciones ejecutadas con sus resultados;
- riesgos restantes y decisiones que siguen correspondiendo al programador.
