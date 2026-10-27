# DYN-03 — Corregir el alcance por sociedad (Company Scoping) en C# / LINQ

**Clase del 27 de octubre de 2026.** Estado inicial: **guía preparada, ejercicio del alumno pendiente**.

## Objetivo y relación con F&O
Detectar y corregir un defecto real **del código del laboratorio**: al elegir `--company DEMF`, el informe de discrepancias sigue incluyendo el voucher `VCH-2026-002` de `USMF` porque `FindFixedDimensionMismatches()` no recibe/fuerza el filtro de sociedad. Aprender **reproduce → isolate root cause → fix → regression test**.

En aplicaciones F&O hay distinción entre *legal entity / company / DataAreaId* y capacidades de consultas entre sociedades. Microsoft documenta `select crossCompany` en X++ y el parámetro `cross-company=true` en OData para escenarios autorizados. **Este programa NO implementa seguridad por empresa: solo corrige el alcance de un informe sobre arrays de prueba.** 
- https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/dev-ref/xpp-data/xpp-select-statement
- https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/odata
- https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/fin-ops/organization-administration/plan-organizational-hierarchy

## Paso 1 — Reproducir el defecto (antes de cambiar código)

Abrir `DynamicsVoucherLab` en Visual Studio, detener una ejecución que aún esté pausada (`Shift+F5`), y abrir **View > Terminal**. Desde la RAÍZ del repositorio clonado:

```powershell
dotnet run --project labs/DYN-02-vouchers-csharp -- --company DEMF --voucher VCH-2026-001
```

Si el terminal está situado directamente en `labs/DYN-02-vouchers-csharp`, utilizar:

```powershell
dotnet run -- --company DEMF --voucher VCH-2026-001
```

**Resultado esperado ANTES de corregir:** el voucher DEMF es válido y balancea 0, PERO en `SIMULATED FIXED DIMENSION MISMATCHES` se ve una alerta de `USMF / VCH-2026-002`. Es el defecto funcional de nuestro demo; no se ha observado aún en la PC del estudiante.

## Paso 2 — Cambiar la llamada (Program.cs, línea ~47)

Antes:
```csharp
var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches();
```

Después:
```csharp
var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches(company);
```

## Paso 3 — Cambiar la firma y el filtro del método (líneas ~109-118)

Antes:
```csharp
public static List<Mismatch> FindFixedDimensionMismatches() =>
```

Después:
```csharp
public static List<Mismatch> FindFixedDimensionMismatches(string company) =>
```

En el `where` de la misma consulta, cambiar:

```csharp
where line.CostCenter != rule.FixedCostCenter
```

por:

```csharp
where header.Company == company && line.CostCenter != rule.FixedCostCenter
```

**Por qué:** ahora el método recibe un argumento `company`, filtra sus resultados por la sociedad elegida y conserva su `JOIN` contra reglas de sociedad + cuenta principal. Esto es **report scoping**, no una regla de autorización.

## Paso 4 — Actualizar las pruebas del propio proyecto

La implementación original llama a `FindFixedDimensionMismatches()` **también** dentro de `LabTests.Run()`. Es un segundo call site que hay que actualizar para no recibir un error de compilación `CS7036: There is no argument given that corresponds to the required parameter 'company'`.

Antes:
```csharp
var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches();
```
En el bloque `LabTests.Run`, reemplazar por:
```csharp
var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches("USMF");
```

Y agregar **dos pruebas nuevas** tras el check original (antes del `Console.WriteLine("\n5/5 checks passed...")`), para comprobar que el filtro funciona:
```csharp
Check(VoucherDiagnostics.FindFixedDimensionMismatches("DEMF").Count == 0,
      "DEMF report does not include USMF discrepancies");
Check(VoucherDiagnostics.FindFixedDimensionMismatches("USMF").Count == 1,
      "USMF report includes its own discrepancy");
```

Actualizar mensajes de salida que indican `five`/`5/5` a **seven** / **7/7** para no confundir los resultados. Alternativa: parametrizar esa cuenta de pruebas, tema futuro.

## Paso 5 — Comprobar en local

Desde la raíz del repositorio:
```powershell
dotnet run --project labs/DYN-02-vouchers-csharp -- --company DEMF --voucher VCH-2026-001
dotnet run --project labs/DYN-02-vouchers-csharp -- --company USMF --voucher VCH-2026-002
dotnet run --project labs/DYN-02-vouchers-csharp -- --test
```

**Esperado después de la corrección:**
- DEMF: sección de mismatches sin ninguna alerta → `No discrepancies in demo data.`
- USMF: reporta `VCH-2026-002`, CC 009 vs 008.
- Tests: **7/7 checks passed.**

La consola comprueba funcionalidad de la simulación, no F&O ni X++.

## Paso 6 — Git local, luego PR o commit

Guardar archivos, mirar la pestaña **Git Changes** y verificar qué cambió. En vez de subir directamente a `main`, preferir crear una rama `feature/company-scoped-mismatches` desde Visual Studio, hacer **Commit** y **Push**, y luego crear un **Pull Request (PR)** en GitHub cuando el alumno domine esta etapa. No comprometer datos sensibles; preservar `main` funcionando.

## Términos para entrevistas ES/EN

| ES | EN |
|---|---|
| Filtrado por sociedad | Company scoping / Legal entity filtering |
| Parámetro del método | Method parameter |
| Argumento de llamada | Method argument |
| Lugar que invoca una función | Call site |
| Error de compilación | Compile-time error |
| Caso de regresión | Regression test |
| Alcance entre sociedades | Cross-company scope |
| Causa raíz | Root cause |

**Respuesta en inglés:**
> I found that a diagnostics report was ignoring the selected legal entity. I reproduced the issue, updated the C# method to accept a company parameter, filtered the LINQ query, and added regression tests to prevent cross-company results from appearing in the wrong report.

**Registro fiel:** solo marcar la práctica terminada cuando el estudiante muestre salida del programa con DEMF y USMF, y 7/7 checks correctos. Hasta entonces, esta es una guía, no una ejecución realizada.
