# Diario de aprendizaje

## 23/10/2026 — DYN-01: factura de proveedor bloqueada por dimensiones
**Estado:** En práctica. **Ambiente:** caso ficticio; sin acceso al sistema para ejecutar.

### Caso
Sociedad ilustrativa USMF; proveedor ficticio V-1001; factura INV-2026-158; cuenta 610100; Departamento FIN; Centro de costos vacío. Se supone que la estructura requiere 101 o 102. No tenemos mensaje de error real ni datos de ningún cliente.

### Respuesta del estudiante
- Si Centro de costos es obligatorio, una combinación vacía no debería contabilizar.
- Verificar otros documentos pendientes afectados; comprobar si se corrige desde la interfaz por un usuario autorizado.
- Confirmar con Finanzas si la configuración contable corresponde o si hay que añadir un centro válido o admitir una excepción.
- Reconoció no saber cómo verificar la **seguridad** de la solución.

### Lo aprendido
El criterio no es solo que la factura se contabilice. Se necesita: aprobación del centro correcto, validación funcional, simulación del asiento, prueba negativa con valores inválidos, prueba positiva con documentos correctos, regresión sobre otras cuentas/sociedades, y autorización antes de producción.

Las dimensiones **predeterminadas** y **fijas** se deben investigar por separado. Una dimensión fija puede afectar el asiento contabilizado aunque una línea muestre otro valor.

### Evidencia pendiente
- [ ] Acceder a demo/sandbox de F&O con permisos suficientes.
- [ ] Capturar la ruta y pantalla de diario de facturas.
- [ ] Comprobar configuración de estructuras contables.
- [ ] Ejecutar Validate y, si está disponible, Simulate posting sin Post.
- [ ] Registrar resultado de una prueba real vs. hipótesis.
- [ ] Continuar con objetos de datos y arquitectura AOT.

[Trello DYN-01](https://trello.com/c/hVHlU4pU)


## 27/10/2026 — DYN-01: diagnóstico del origen de dimensiones en Invoice Journal
**Respuesta del estudiante:** «Hay que revisar ambas configuraciones, proveedor y cuenta para ver dónde está el conflicto, de dónde vienen los datos».

**Devolución:** correcto como punto de partida; ampliar la trazabilidad al nombre de diario, encabezado del diario, cuenta de la línea, cuenta de contrapartida, dimensiones predeterminadas y fijas, estructuras contables, reglas derivadas y posibles personalizaciones.

**Fundamento Microsoft Learn:** el nombre del diario predetermina el encabezado; la cuenta de línea hereda valores del encabezado y rellena blancos desde el proveedor u otro maestro; la cuenta de contrapartida toma primero dimensiones de la línea y completa valores faltantes; las dimensiones *Fixed* en las cuentas principales se imponen al contabilizar. Referencia: https://learn.microsoft.com/es-es/dynamics365/finance/general-ledger/dimensions-default-values .

**Estado:** interpretación conceptual aprobada; sin transacción real ni pruebas realizadas. Siguiente ejercicio: contraste de dimensiones visibles en línea vs. dimensiones del asiento con *Fixed*.


## 27/10/2026 — Primera ejecución local del laboratorio C# confirmada

**Evidencia:** captura compartida por estudiante con consola de Visual Studio.

- Proyecto `labs/DYN-02-vouchers-csharp/DynamicsVoucherLab.csproj` abierto desde el repositorio clonado.
- Compilación **Build succeeded**: 1 proyecto correcto, 0 fallidos.
- Aplicación **termina con Exit code 0**.
- Voucher `VCH-2026-001` para `USMF`: encabezado RecId `1001`; movimientos RecId `5001` (gasto `606300`, Department `022`, CostCenter `008`) y RecId `5002` (pasivo `201100`, Department `022`, CostCenter `009`).
- Conciliación `Balance: 0.00 (BALANCED)`.
- Detección ilustrativa: voucher `VCH-2026-002` con CostCenter `009` vs Fixed `008` bajo regla actual ficticia.
- **Diferenciar:** esto es ejecución C# local con datos en memoria, NO consulta real a F&O ni X++.
- El estudiante colocó breakpoint en `var rows = VoucherDiagnostics.FindVoucher(company, voucher);`, pero la captura solo demuestra ejecución completa (sin pausa de debugging). **Debugging pendiente**: usar `Debug > Start Debugging` / F5 sin Ctrl, verificar flecha amarilla y `Locals` (`company=USMF`, `voucher=VCH-2026-001`), luego F11 para entrar al método y analizar LINQ.

**Siguiente objetivo técnico:** comprender y explicar la relación 1:N por `GeneralJournalAccountEntry.GeneralJournalEntry` a `GeneralJournalEntry.RecId`, filtrar por sociedad y aprender la diferencia entre **Start Without Debugging (Ctrl+F5)** y **Start Debugging (F5)**.


## 27/10/2026 — Primer breakpoint de C# alcanzado en Visual Studio

**Evidencia:** captura aportada por el estudiante muestra **flecha amarilla de ejecución** y la línea 26 resaltada:

```csharp
var rows = VoucherDiagnostics.FindVoucher(company, voucher);
```

**Logro confirmado:** la aplicación está **pausada en el depurador (Start Debugging / F5)**, a diferencia de la ejecución previa con Ctrl+F5. Esta línea todavía no ejecutó `FindVoucher`, por lo que `rows` aún no tiene el resultado.

**Siguiente acción práctica:** pasar el mouse sobre `company` y `voucher` y verificar los valores esperados `USMF` y `VCH-2026-001`; luego **F11 — Step Into** una sola vez para entrar al método `VoucherDiagnostics.FindVoucher` y observar el LINQ JOIN `header.RecId equals line.GeneralJournalEntryId`. Al pulsar **F10 — Step Over** sobre la expresión que termina en `.ToList()`, la consulta materializa `List<VoucherRow>` y, al regresar, se podrá inspeccionar `rows.Count` y los movimientos contables. **No atribuir al estudiante esta segunda inspección hasta ver evidencia.**

Terminología EN/ES: breakpoint/punto de interrupción; current statement/próxima instrucción; step into/entrar al método; locals/variables locales; step over/ejecutar siguiente instrucción; method call/llamada a método.

**Estado:** Debugger breakpoint confirmado; inspección de variables y F11 pendientes; sin ejecución X++ ni F&O real.


## 27/10/2026 — Step Into confirmado en FindVoucher

**Evidencia:** captura de Visual Studio con flecha amarilla en **línea 100** de `Program.cs`, dentro de `VoucherDiagnostics.FindVoucher(string company,string voucher)`, a la altura de la consulta LINQ (método `=> (...).ToList()`). El depurador muestra `company = "USMF"`. **Hito F11 / Step Into logrado**.

**Consulta vista:**
```csharp
from header in DemoData.Headers
join line in DemoData.Lines
    on header.RecId equals line.GeneralJournalEntryId
where header.Company == company && header.SubledgerVoucher == voucher
orderby line.RecId
select new VoucherRow(header.RecId, line.RecId, line.MainAccount,
                      line.Department, line.CostCenter,
                      line.AccountingCurrencyAmount)
```
`ToList()` ejecuta y materializa la consulta. Se explicó `from`/`join`/`where`/`orderby`/`select` y equivalencia a `SQL INNER JOIN` con filtro por sociedad y voucher. **Modelo didáctico:** `GeneralJournalEntry` (header RecId=1001) → dos líneas `GeneralJournalAccountEntry` (RecId 5001, 5002), relación `line.GeneralJournalEntryId = header.RecId`. En F&O real, campo de relación `GeneralJournalAccountEntry.GeneralJournalEntry`.

**Próxima acción:** en pausa, **F10 — Step Over** una vez para ejecutar la consulta entera (método de una sola expresión) y regresar al código llamador, habitualmente `if (rows.Count == 0)`. Inspeccionar en Locals/hover `rows.Count = 2` y elementos [0] y [1] y sus atributos. Los valores son **esperados**, no observados todavía; esperar captura.

Terminología de entrevista: **Step Into, Step Over, LINQ, materialize results, 1-to-many join, record identifier, debugger watch/locals**. No hubo ejecución contra F&O ni compilación de X++.


## 27/10/2026 — Se materializó y se inspeccionó la lista devuelta por LINQ

**Evidencia:** captura de Visual Studio, durante depuración, con el tooltip "FindVoucher returned" y **Count=2** tras usar Step Over. El estudiante expandió la colección y se ven dos elementos:

| Objeto | HeaderRecId | LineRecId | MainAccount | Department | CostCenter |
|---|---|---|---|---|---|
| `rows[0]` | `1001` | `5001` | `606300` | `022` | `008` |
| `rows[1]` | `1001` | `5002` | `201100` | `022` | `009` |

Se comprueba la **cardinalidad 1:N (one-to-many relationship)** entre encabezado (`GeneralJournalEntry`) y movimientos (`GeneralJournalAccountEntry`) mediante `RecId`, representada en un `LINQ join`. `ToList()` materializó la consulta y devolvió `List<VoucherRow>`. Este resultado es de **datos ficticios en memoria** (C#); no es salida de un entorno real de F&O.

**Hitos confirmados:** clonación, proyecto abierto, compilación, ejecución local, breakpoint, F11 Step Into, F10 Step Over, inspección de `List<VoucherRow>` y Count=2. El panel mostrado incluye además herramientas del debugger como Call Stack/Autos.

**Próxima práctica propuesta:** usar `Debug > Windows > Watch > Watch 1` con expresiones `rows.Count`, `rows[0].HeaderRecId` y `rows[1].HeaderRecId`; verificar que ambas líneas apuntan a 1001. Luego se podrá analizar `FindFixedDimensionMismatches()` y su segundo `join` contra reglas de dimensión ficticias. No marcar aún la práctica Watch como completada.

**Inglés:** query result, list/collection, item, property, one-to-many relationship, primary key, foreign key, runtime inspection, materialization.
