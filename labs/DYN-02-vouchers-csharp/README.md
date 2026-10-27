# DYN-02 — Diagnóstico de vouchers con C# / LINQ (Visual Studio local)

**Objetivo:** empezar a pensar como `Functional Technical Consultant / Developer` de Dynamics 365 Finance, con consultas y verificaciones verdaderamente **ejecutables**, sin instalar un ERP o un contenedor en la PC.

**Se necesita:** Visual Studio con soporte para proyectos .NET 8 o el SDK .NET 8 ya disponible. **Sin paquetes NuGet externos**, sin Docker, sin SQL Server, sin Python y sin acceso a Finance. Si el SDK no está instalado, la compilación no funcionará; comprobar antes de instalar nada.

## En Visual Studio (IDE completo)
1. Cloná https://github.com/gastonferreira125-rgb/dynamics-365-consultor-developer-lab desde **Clone a repository**, o descargá el ZIP del repositorio si no tenés Git configurado.
2. Elegí **File > Open > Project/Solution** y abrí `labs/DYN-02-vouchers-csharp/DynamicsVoucherLab.csproj`.
3. Presioná **Ctrl+F5** (*Start without debugging*) para correr el caso `USMF / VCH-2026-001`.
4. Poné un **breakpoint** dentro de `FindVoucher` y presioná **F5** (*Start debugging*). Seguí `header`, `line` y el resultado del `join`.
5. Para elegir otro voucher: en propiedades de depuración del proyecto, configurá los **Command line arguments** `--company USMF --voucher VCH-2026-002`; o usá una terminal como abajo.

## Alternativa: terminal de Visual Studio o VS Code
Desde la carpeta raíz del repositorio:
```powershell
dotnet run --project labs/DYN-02-vouchers-csharp
dotnet run --project labs/DYN-02-vouchers-csharp -- --company USMF --voucher VCH-2026-002
dotnet run --project labs/DYN-02-vouchers-csharp -- --test
```
El separador `--` después de la ruta envía los parámetros a **nuestro programa** y no al comando dotnet.

## Qué esperamos ver
- **001 / USMF:** 2 movimientos, Dr +1.000 / Cr −1.000, resultado balance 0; la cuenta de gasto 606300 lleva CostCenter=008.
- **002 / USMF:** Dr +750 / Cr −750; balance 0, pero CostCenter=009 en gasto 606300, diferente de Fixed=008 **según la configuración de ejemplo**.
- **001 / DEMF:** voucher con el mismo texto pero diferente sociedad e identificador interno.
- `--test`: **5/5 checks passed**. Son checks sobre datos sintéticos (no unit tests de F&O).

## Cómo relacionarlo con F&O real

| Nuestro código | F&O real / concepto |
|---|---|
| `GeneralJournalEntry` | Encabezado del asiento contable |
| `GeneralJournalAccountEntry` | Movimientos contables por cuenta |
| `GeneralJournalEntryId` | Campo ficticio que representa la FK real `GeneralJournalAccountEntry.GeneralJournalEntry` |
| `RecId` | Identificador técnico del registro |
| `join ... on ... equals ...` | Relación similar a un `JOIN` SQL / `join` X++ |
| `MainAccount`, `CostCenter` como textos | **Simplificación:** en Finance se resuelven desde `LedgerDimension` y tablas/servicios de dimensiones; no son esas columnas directas |
| `FixedRules` | Tabla inventada para practicar una comparación; no reemplaza la configuración real en `Legal entity overrides` |

**Importante:** encontrar un asiento histórico con CC 009 frente a una regla actual 008 **no demuestra que el asiento se contabilizó erróneamente**. Investigar fecha de cambios, sociedad, cuenta, origen del asiento y reglas de dimensión. El programa **no se conecta** a Microsoft Dynamics y **no compila X++**.

## Entrevista — frase útil

> I use C# and LINQ to join general journal headers with account entries, filter by legal entity, reconcile debit and credit amounts, and flag unexpected financial dimensions. For Dynamics 365 Finance, I would then confirm the actual posting setup and trace the voucher in the application.

## Fuentes
- Microsoft Learn, [Default financial dimensions](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/dimensions-default-values)
- [Troubleshooting general journal entries](https://learn.microsoft.com/en-us/troubleshoot/dynamics-365/finance/business-performance-analytics/missing-journal-entries-err00004)

**Evaluación:** correr el programa local y enviar captura de `Program.cs` más ventana de salida. Registrar luego en Trello lo que realmente se ejecutó.


## Solución a error Git fatal en Visual Studio — URL con parámetros de seguimiento

Si aparece `Git failed with a fatal error. ...?utm_source=chatgpt.com/info/refs not valid. is this a git repository?`, normalmente **la dirección copiada incluye parámetros de seguimiento** que rompen la URL usada por Git al consultar `info/refs`. No es un defecto del código C# ni hace falta instalar otra herramienta.

**URL exacta para pegar en Visual Studio > Clone a repository** (sin query string):

```text
https://github.com/gastonferreira125-rgb/dynamics-365-consultor-developer-lab.git
```

Borrar antes **todo** el contenido del campo `Repository location`, pegar esta dirección limpia y volver a pulsar **Clone**. Evitar copiar la URL directamente desde la barra de navegación si termina con `?utm_source=...` u otros parámetros. El sufijo `.git` es válido para clonar. El repositorio es público, por lo que no debería exigir credenciales solo para lectura. Una vez clonado, abrir `labs/DYN-02-vouchers-csharp/DynamicsVoucherLab.csproj`.

**Evidencia:** alumno mostró captura con cadena `?utm_source=chatgpt.com/info/refs`, compatible con URL de clonación contaminada. **No se confirmó todavía que el nuevo intento haya terminado bien.**
