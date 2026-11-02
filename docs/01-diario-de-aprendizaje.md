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


## 27/10/2026 — Watch 1: 4 verificaciones confirmadas en Visual Studio

**Evidencia:** captura del estudiante muestra F10 completado y ejecución detenida en `Program.cs` línea 27 `if (rows.Count == 0)`, con condición evaluada `false`. En la ventana Watch 1 aparecen las siguientes expresiones y valores comprobados:

| Watch expression | Valor observado | Tipo |
|---|---|---|
| `rows[0].HeaderRecId` | `1001` | `long` |
| `rows.Count` | `2` | `int` |
| `rows[1].HeaderRecId` | `1001` | `long` |
| `rows[0].Amount + rows[1].Amount` | `0` | `decimal` |

**Hito:** ya no son expectativas: Watch muestra las cuatro comprobaciones reales del código C# local. La consulta LINQ produjo dos filas que apuntan al mismo encabezado; los importes se compensan. **Un voucher balanceado puede igualmente tener dimensiones financieras equivocadas.** No se ha conectado a un F&O real.

**Próxima práctica (pendiente):** colocar un nuevo breakpoint en la invocación `var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches();` mediante Ctrl+F, F9; F5 para continuar desde la línea 27 y detenerse en esa segunda llamada; luego F11 Step Into. Explicar los dos `join` de LINQ: Header a AccountEntry por RecId, luego AccountEntry contra FixedRules usando clave compuesta `Company + MainAccount`; `where line.CostCenter != rule.FixedCostCenter` filtra discrepancias. Resultado esperado: USMF, voucher `VCH-2026-002`, CC registrado `009` vs Fixed esperado `008`. La regla de Fixed es ficticia y actual, sin valor como prueba histórica de F&O.

**Inglés nuevo:** *watch expression*, *conditional branch*, *balanced voucher*, *composite join key*, *fixed dimension mismatch*, *historical configuration*.


## 27/10/2026 — Step Into confirmado en FindFixedDimensionMismatches()

**Evidencia:** captura del alumno en Visual Studio; la flecha amarilla está en la **línea 110** de `Program.cs`, dentro de `VoucherDiagnostics.FindFixedDimensionMismatches()`. Se ha ejecutado **F11 — Step Into** desde la invocación del método. **Todavía no se ha ejecutado la expresión `.ToList()` ni observado el resultado del segundo JOIN en Watch.**

**Consulta que el alumno tiene abierta:**
```csharp
from header in DemoData.Headers
join line in DemoData.Lines on header.RecId equals line.GeneralJournalEntryId
join rule in DemoData.FixedRules
    on new { header.Company, line.MainAccount }
    equals new { rule.Company, rule.MainAccount }
where line.CostCenter != rule.FixedCostCenter
orderby header.Company, header.SubledgerVoucher
select new Mismatch(header.Company, header.SubledgerVoucher,
                    line.MainAccount, line.CostCenter,
                    rule.FixedCostCenter)
```

**Explicación bilingüe:** primer join = `Header→AccountEntry` por identificador interno, segundo join = `AccountEntry→Fixed dimension rules` por **composite join key / clave de unión compuesta** de sociedad + cuenta. `where ... != ...` = filtro de diferencias. `new { ... }` en C# representa un **anonymous type / tipo anónimo**. `ToList()` = **query materialization / materialización de resultados**.

**Siguiente instrucción:** pulsar F10 (**Step Over**) una vez, normalmente retorna al llamador antes de la instrucción siguiente, y examinar en `Watch 1`: `mismatches.Count` (1), `mismatches[0].Company` ("USMF"), `mismatches[0].Voucher` ("VCH-2026-002"), `mismatches[0].MainAccount` ("606300"), `mismatches[0].Actual` ("009") y `mismatches[0].Expected` ("008"). Valores **esperados**, todavía sin evidencia de salida observada.

**Advertencia:** `FixedRules` es una estructura inventada para este lab en memoria. Un conflicto con las reglas ficticias actuales no demuestra un error histórico contable en Dynamics real. Nada de X++ ni F&O real ejecutado.


## 27/10/2026 — Depuración de alcance de variable (Variable Scope)

**Evidencia:** screenshot durante depuración en `FindFixedDimensionMismatches()` línea 110, con Watch 1 mostrando `error CS0103: The name 'mismatches' does not exist in the current context` para `mismatches.Count`, `mismatches[0].Company`, `mismatches[0].Voucher`, `mismatches[0].Actual`, `mismatches[0].Expected`.

**Diagnóstico preciso:** la ejecución está en el método **callee** `FindFixedDimensionMismatches()`; la variable local `mismatches` pertenece al **caller** (bloque principal o *top-level statements* de `Program.cs`), donde se declara `var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches();`. Por lo tanto, no está disponible en el ámbito (*scope*) del método actual. **No es error de compilación ni del JOIN.**

**Resolución instruida, pendiente de confirmar:** pulsar **F10 — Step Over** una vez para terminar la expresión `(...).ToList()` y regresar al caller tras la asignación; inspeccionar Watch allí. Resultado esperado `Count=1`, sociedad USMF, voucher VCH-2026-002, diferencia CostCenter 009 vs Fixed 008. No afirmar que se verificaron todavía.

**Conceptos EN:** variable scope, local variable, caller, callee, stack frame, Watch window, Step Over.


## 27/10/2026 — DYN-02, validación de inconsistencias de dimensiones finalizada

**Evidencia de ejecución local en Visual Studio:** última captura del usuario, con debugger pausado en `Program.cs` línea 48 (`foreach (var issue in mismatches)`) y ventana **Watch 1** mostrando, ya dentro del `Main`, los valores **confirmados**:

| Variable verificada | Valor |
|---|---|
| `mismatches.Count` | `1` |
| `mismatches[0].Company` | `"USMF"` |
| `mismatches[0].Voucher` | `"VCH-2026-002"` |
| `mismatches[0].Actual` | `"009"` |
| `mismatches[0].Expected` | `"008"` |

**Estado:** se completaron las prácticas de local C#: compilación, ejecución, F5 con breakpoint, F11 Step Into, F10 Step Over, `Watch 1` con resultados, consultas LINQ con 1 y 2 JOINs, clave compuesta (company/main account), comparación de dimensiones y resolución del error de scope `CS0103`. Los resultados corresponden a **datos simulados, no a un entorno real de Microsoft Dynamics 365 Finance**. Las cinco verificaciones del proyecto también pasaron en CI GitHub Actions y un voucher se confirmó balanceado.

**Aprendizaje funcional:** un voucher con débitos/créditos equilibrados puede tener dimensiones erróneas; en F&O real hay que verificar sociedad, cuenta, versión histórica de la configuración Fixed y valores contables en el sistema antes de sugerir ajustes.

**Resultado laboral:** evidencia preparada para un post bilingüe LinkedIn con capturas auténticas de Visual Studio. Posicionamiento: consultor funcional ERP con aprendizaje técnico en C#/.NET/LINQ y troubleshooting; no afirmar desarrollo X++ ni conexión live a F&O.

**Siguiente módulo técnico:** código C# para consultar datos desde una fuente externa/autorizada y aprender a resolver LedgerDimension; X++ únicamente cuando haya developer environment F&O.


## 02/11/2026 — LAB-TECH-02: reproducción del error confirmada
Captura del estudiante ejecutando en Visual Studio Developer PowerShell: `dotnet run -- --company DEMF --voucher VCH-2026-001` desde `labs/DYN-02-vouchers-csharp`.
Resultado observado: DEMF, header RecId 2001, líneas RecId 6001 (606300 CC012 +200) y 6002 (201100 CC012 -200), balance 0.00 BALANCED. El apartado de anomalías incluye indebidamente `USMF / VCH-2026-002`, posted CC009 vs Fixed CC008. Root cause: `FindFixedDimensionMismatches()` no recibe ni filtra `company`. **Error reproducido, NO corregido todavía**. Próximo paso: pasar `company` al método y filtrar por sociedad; actualizar el call site en los tests y agregar pruebas de regresión para USMF y DEMF. Es un lab C# con datos ficticios, no F&O real.


## 02/11/2026 — LAB-TECH-02: prueba funcional DEMF aprobada (C# local)
**Captura aportada por el estudiante:** en Visual Studio Developer PowerShell, dentro del proyecto C#, se ejecutó `dotnet run -- --company DEMF --voucher VCH-2026-001` después de editar el método `FindFixedDimensionMismatches` para filtrar por sociedad.
**Salida observada:** `Legal entity: DEMF`, header `RecId 2001`, líneas `6001/6002`, importes `+200.00/-200.00`, `Reconciliation / Balance: 0.00 (BALANCED)` y `No discrepancies in demo data.` **El reporte ya no presenta la alerta de USMF** que sí aparecía antes de la corrección. Estado: **prueba funcional DEMF pasada**, sin evidencia todavía de prueba USMF ni de regression tests finales. El código C# modificado reside en la copia local del usuario, NO se ha recibido commit/push de esos cambios a GitHub. No se probó F&O real.
**Próximo paso:** ejecutar `dotnet run -- --company USMF --voucher VCH-2026-002` y confirmar que sigue apareciendo el mismatch CC 009 vs Fixed 008; luego ejecutar `dotnet run -- --test`, ampliar controles a 7/7 y finalmente hacer commit/push de los cambios verificados.


## 02/11/2026 — LAB-TECH-02: prueba funcional USMF aprobada
Captura del alumno desde Developer PowerShell, después de corregir el filtro en su Visual Studio local. Se ejecutó `dotnet run -- --company USMF --voucher VCH-2026-002` en `labs/DYN-02-vouchers-csharp`.
**Evidencia observada:** `Legal entity: USMF | Voucher: VCH-2026-002`; Header RecId `1002`; líneas `5003` (cuenta 606300, Department 022, CostCenter 009, importe +750.00) y `5004` (cuenta 201100, Department 022, CostCenter 009, -750.00); `Reconciliation / Balance: 0.00 (BALANCED)`; reporte `USMF / VCH-2026-002 | Main account 606300 | Posted CC 009 vs. currently configured Fixed CC 008`.
**Estado verificado:** ambas pruebas funcionales DEMF y USMF PASARON según capturas. El alumno corrigió el filtrado por sociedad en su copia LOCAL de `Program.cs`. **Aún pendientes:** añadir 2 controles automatizados al método `LabTests.Run()` (pasar de 5 a 7 checks), ejecutar `dotnet run -- --test`, revisar `Git Changes`, crear commit y push de la modificación local a GitHub. La versión remota del código no ha sido modificada por esta corrección; tampoco hubo acceso a un entorno real de Dynamics F&O.
**Inglés:** regression test, company scoping, root cause, fixed dimension mismatch, expected result, actual result.


## 02/11/2026 — LAB-TECH-02: pruebas de regresión 7/7 confirmadas en Visual Studio

**Evidencia:** captura real del estudiante ejecutando `dotnet run -- --test` en Developer PowerShell, desde `labs/DYN-02-vouchers-csharp`. La consola informa **Running seven checks on SIMULATED data** y **7/7 checks passed. Not an F&O integration test.** La salida de los siete `PASS` aparece dos veces en el historial de la consola.

Verificaciones observadas:
1. Header JOIN returns two accounting entries.
2. Expense account on voucher 001 has fixed cost center 008.
3. Filter by legal entity prevents cross-company voucher confusion.
4. All three fictitious vouchers balance.
5. A discrepancy is detected for voucher 002.
6. DEMF must not show USMF discrepancies.
7. USMF must retain its own discrepancy.

**Estado del aprendizaje:** `Reproduce → Diagnose → Fix → Regression Test` completado en C# local. Las pruebas previas DEMF y USMF también se confirmaron por capturas. Las pruebas usan datos **simulados**; no se accedió a F&O ni se ejecutó X++.

**PENDIENTE:** publicar la modificación `Program.cs` realizada por el estudiante en su copia local. Por ahora, el repositorio remoto contiene material de enseñanza y el código original; el nuevo filtro de empresa aún no fue confirmado en GitHub. Ruta recomendada para aprender Git: crear una rama `fix/company-scoped-mismatches`, revisar `Git Changes`, registrar un commit solo con el código pertinente, **Push** de la rama y abrir un Pull Request contra `main`. Como `main` remoto ha recibido cambios en documentos desde la clonación, evitar copiar/pegar o sobrescribir archivos ajenos y preferir un PR.


## 02/11/2026 — LAB-TECH-02: rama Git local y cambios detectados
**Evidencia:** captura del panel Git Changes de Visual Studio. Rama activa `fix/company-scoped-mismatches`; `Changes (1)` muestra únicamente `labs/DYN-02-vouchers-csharp/Program.cs` con estado `M` (Modified). En el encabezado Visual Studio muestra aviso `Configure your user name and email address before committing changes`.
**Estado confirmado:** rama de trabajo local creada; archivo de la corrección identificado como modificado. **Pendiente:** configurar identidad Git local con dirección verificada/privada de GitHub, revisar diferencias, registrar commit, hacer push de la rama y abrir Pull Request. No afirmar que estos pasos ya se completaron. Aconsejado usar email noreply si desea proteger su correo personal. Se conservan pruebas funcionales DEMF/USMF y 7/7 regression checks verificadas anteriormente en ejecución local.


## 02/11/2026 — LAB-TECH-02: revisión visual del Git Diff, antes de commit
El usuario mostró captura de **Diff - Program.cs** en Visual Studio 2026, con 6 bloques de cambios (+19/-6). En el fragmento visible de `LabTests.Run()` se observa la nueva invocación `FindFixedDimensionMismatches("USMF")`, las dos nuevas comprobaciones DEMF sin mismatches y USMF con una discrepancia, y el mensaje `7/7 checks passed`. En capturas anteriores se había verificado la ejecución local con 7/7 pruebas aprobadas. No se ha revisado visualmente cada uno de los seis bloques de este diff completo, pero las pruebas de ejecución apoyan la corrección. Siguiente paso indicado: en rama local `fix/company-scoped-mismatches`, comprobar que Git Changes incluya solo `Program.cs`, hacer **Commit All** con mensaje `fix: filter voucher discrepancies by legal entity`; luego **Push** de esa rama y abrir PR hacia main. **No hay commit/push/PR confirmados todavía**. Código original remoto permanece sin actualizar por el alumno.


## 02/11/2026 — LAB-TECH-02: primer commit local confirmado
**Evidencia:** captura de Visual Studio Git Changes confirma banner `Commit b1e1ccf5 created locally`, rama `fix/company-scoped-mismatches`, indicador `1/0` (un commit local por publicar) y mensaje `There are no unstaged changes in the working directory`. Las 7 pruebas del laboratorio C# habían pasado en capturas previas.
**Estado:** Commit LOCAL completado; **Push aún no confirmado** ni Pull Request creado. El próximo paso es usar la flecha ascendente **Push / Publish Branch** en Git Changes para publicar esta rama en GitHub, dejando `main` intacta. Después abrir un PR y verificar que los cambios se limiten a la corrección de Program.cs. No afirmar publicación remota antes de comprobarlo.

## 02/11/2026 — LAB-TECH-02: Push remoto verificado y CI verde
**Evidencia:** captura del alumno en Visual Studio Git Changes: Successfully pushed fix/company-scoped-mismatches to origin, indicador 0/0 y working tree limpio. Incluye opción Create pull request.
**Verificación directa en GitHub:** la rama remota fix/company-scoped-mismatches existe; Program.cs incluye la llamada con argumento company, firma FindFixedDimensionMismatches(string company), filtro LINQ por sociedad, 2 controles de regresión y texto 7/7.
**CI:** GitHub Actions completado con éxito: https://github.com/gastonferreira125-rgb/dynamics-365-consultor-developer-lab/actions/runs/41460118496
**Comparación main...fix/company-scoped-mismatches:** 1 solo archivo modificado (labs/DYN-02-vouchers-csharp/Program.cs, +19/-6), 1 commit de corrección y 18 commits en main que la rama aún no incorpora. Esta divergencia no afecta el éxito del Push.
**Pendiente:** alumno creará su primer Pull Request desde Create in browser; verificar base=main y compare=fix/company-scoped-mismatches, título fix: filter voucher discrepancies by legal entity. Revisar PR y checks antes de Merge.
**Inglés:** push, feature branch, compare changes, base/head, pull request, CI checks, merge.

## 02/11/2026 — Primer Pull Request #1 creado y revisado
**Evidencia:** captura del alumno en GitHub y verificación del PR por el conector. PR: https://github.com/gastonferreira125-rgb/dynamics-365-consultor-developer-lab/pull/1
- Título: fix: filter voucher discrepancies by legal entity.
- Base `main`, head `fix/company-scoped-mismatches`, un commit (`b1e1ccf5`), un archivo cambiado: `labs/DYN-02-vouchers-csharp/Program.cs` (+19/-6).
- GitHub reporta PR **open**, `mergeable=true` y `mergeable_state=clean`, sin conflictos. Checks exitosos; CI de la rama: https://github.com/gastonferreira125-rgb/dynamics-365-consultor-developer-lab/actions/runs/41460118496
- Revisión del diff: caller pasa `company`; el método recibe `string company`; el filtro LINQ exige `header.Company == company`; pruebas DEMF y USMF añadidas; mensajes 7/7.
- **Estado:** PR apto para integración, **NO fusionado todavía** al momento de la verificación. Se indicó al alumno Merge pull request > Confirm merge, y después cambiar a `main` en Visual Studio y hacer Pull.
- El laboratorio sigue siendo C# con datos sintéticos: no se ejecutó un ERP real ni X++.

## 02/11/2026 — LAB-TECH-02 terminado: PR #1 integrado en main
**Evidencia del alumno:** captura de GitHub con estado `Merged` y mensaje `Pull request successfully merged and closed` en PR #1.
**Verificación directa por integración GitHub:** https://github.com/gastonferreira125-rgb/dynamics-365-consultor-developer-lab/pull/1 indica `state=closed`, `merged=true`, `merged_at=2026-11-02T14:23:11Z`, merge commit `4fe1e4a13338366d06e10dd0f4d7ca7912a98cc1`.
**Código main verificado:** `labs/DYN-02-vouchers-csharp/Program.cs` ya contiene el método `FindFixedDimensionMismatches(string company)`, el filtro `header.Company == company`, dos nuevos controles DEMF y USMF y mensaje `7/7 checks passed`.
**Hitos demostrados por capturas:** reproducción del bug, inspección con debugger, corrección por legal entity, dos pruebas funcionales, 7/7 regression checks locales, Git branch, commit, push, PR #1, CI exitoso y merge.
**Nota de alcance:** aplicación C# con datos ficticios inspirada en Finance; no hay prueba sobre Dynamics real ni desarrollo X++ ejecutado.
**Siguiente paso local pendiente:** cambiar a la rama `main` en Visual Studio y hacer `Git > Pull` para sincronizar con remoto. Luego ejecutar `dotnet run -- --test` para volver a confirmar el estado actualizado de main. No marcar sincronización local hasta evidencia.
**Términos EN:** merged pull request, main branch, sync, pull, regression testing, CI/CD, code review.


## 02/11/2026 — LAB-TECH-02: pendiente sincronización local de main
**Nueva evidencia del estudiante:** captura de Visual Studio Developer PowerShell, ejecutando `dotnet run -- --test` en la carpeta `labs/DYN-02-vouchers-csharp`. La salida muestra **Running five checks** y **5/5 checks passed**, dos veces; no aparece la versión esperada de 7 pruebas.
**Diagnóstico:** el proyecto local que se está ejecutando aún contiene la versión original de cinco pruebas, ya sea por estar en main local desactualizada u otra rama/copia. **No inferir la rama activa de la captura de terminal.** Se verificó que `main` REMOTO de GitHub sí contiene `FindFixedDimensionMismatches(string company)` y siete pruebas (7/7). Se indicó comprobar en terminal `git branch --show-current` y `git status`; si la rama activa es `main`, ejecutar `git pull origin main`, y volver a probar `dotnet run -- --test`. Si está en feature, primero cambiar de forma segura a main. **No se confirmó aún el Pull ni los siete tests en main local.**


## 02/11/2026 — Git local: Detached HEAD y comando git no disponible
**Evidencia de captura:** Visual Studio muestra `Detached at b0a5ded0` en Git Changes y `Your checkout completed successfully` después de seleccionar un commit histórico. Developer PowerShell rechaza `git branch --show-current`, `git status` y `git pull origin main` con `CommandNotFoundException` porque `git` no está en la ruta ejecutable de esa terminal.
**Diagnóstico:** el checkout realizado fue a un commit antiguo y NO al nombre de la rama principal. Esto explica que el programa local siga mostrando 5/5 pruebas, mientras en GitHub remoto `main` ya tiene 7/7. No afirmar que se haya sincronizado hasta nueva captura.
**Acción guiada por GUI Visual Studio:** clic derecho sobre la rama `main` en Git Repository > Checkout; verificar que el indicador deje de decir Detached, luego menú Git > Pull. Ejecutar nuevamente `dotnet run -- --test` (el comando dotnet sí funciona). Evitar intentar `git` en esta terminal e instalar Git innecesariamente: Visual Studio ofrece GUI Git funcional.
**Pendiente:** verificar que la rama main se ha seleccionado, que Pull fue exitoso y que el test local muestra 7/7. No alterar historial con Reset ni Revert.


## 02/11/2026 — Sincronización local de main validada con siete pruebas
**Evidencia del estudiante:** captura Developer PowerShell desde `labs/DYN-02-vouchers-csharp` con ejecución de `dotnet run -- --test`: se muestran las siete comprobaciones PASS y la línea **7/7 checks passed. Not an F&O integration test.** La captura previa confirma `main` seleccionada en la interfaz Visual Studio.
**Interpretación:** la copia local ya ejecuta la versión de siete pruebas incorporada mediante PR #1 a main. La parte superior de la consola mantiene un error previo `git no se reconoce` por falta de git CLI en PATH, pero no afecta la ejecución .NET ni el Git GUI de Visual Studio.
**Estado:** la actualización de código local es efectiva, LAB-TECH-02 completamente cerrado y verificado; no declarar verificado el paso exacto `Git > Pull` solamente por la salida, aunque el resultado corresponde a la versión ya fusionada en main.
**Próxima etapa:** LAB-TECH-03 integraciones OData / HTTP GET / JSON en C# sin ERP instalado. Se utilizará una API de prueba OData v4 pública, claramente separada de F&O real; luego vincular con Data Entities, OData /data, dataAreaId, OAuth2 de F&O.


## 02/11/2026 — LAB-TECH-03: primera consulta HTTP GET/OData comprobada
El estudiante abrió el endpoint público `https://services.odata.org/V4/TripPinServiceRW/People?$top=3` en su navegador y compartió el **JSON completo**, con `@odata.context` y el arreglo `value` con tres personas: `russellwhyte`, `scottketchum` y `ronaldmundy`. Se observan propiedades `UserName`, `FirstName`, `LastName`, `Emails`, `AddressInfo` y metadatos `@odata.etag`. Esto confirma respuesta real de un servicio público OData de demostración (**NO Dynamics 365 Finance**).
**Conceptos aprendidos:** HTTP GET, OData service root, entity set `People`, query option `$top=3`, JSON object/array, metadata context, ETag. **Próxima práctica pendiente:** crear un cliente C# Console App .NET 8 con `HttpClient`, `await`, `JsonDocument` y consulta `$select=UserName,FirstName,LastName`. No afirmar ejecución C# hasta recibir evidencia.
**Conexión F&O:** Data Entities públicas en `/data`, colecciones determinadas por metadata, requieren OAuth/permisos; sintaxis y autenticación explicadas separadamente.
