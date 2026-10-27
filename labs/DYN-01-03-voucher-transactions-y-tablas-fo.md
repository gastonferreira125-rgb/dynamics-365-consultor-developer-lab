# DYN-01 — Clase 3 | Journal → Posting → Voucher transactions (ES/EN)

**Fecha:** 27/10/2026. **Modalidad:** pantallas oficiales + caso simulado, **no se operó un ambiente F&O**.
**Trello:** https://trello.com/c/hVHlU4pU

## Objetivos
- Comprender la diferencia entre **journal line** (línea ingresada) y **posted ledger account entry** (asiento en contabilidad general).
- Navegar hacia **Voucher transactions** y **Transaction origin** para investigar incidencias.
- Reconocer las primeras tablas de F&O antes y después de contabilizar.
- Practicar terminología profesional en inglés.

## Pantalla real
Captura de **Journal voucher** de Microsoft Learn: https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/media/multi-line.png

Microsoft confirma la ruta **General ledger > Inquiries and reports > Voucher transactions**, con filtros por fecha, cuenta, comprobante y acceso a **Transaction origin** y **Original document**.
Fuente: https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/tasks/view-journal-entries-or-transactions

**Diferencias terminológicas:**
- **Invoice number**: identificador de factura, no necesariamente igual a Voucher.
- **Voucher**: identificador del comprobante contable; puede agrupar varias accounting entries.
- **Journal batch number / Journal number**: identificadores de agrupación de diario; no asumir que son el voucher ni que todos los números de diario de distintas pantallas coinciden.

## Laboratorio ficticio (sin impuestos para aislar el concepto)

Cuenta Vendor: `US-111`.
Cuenta Ledger de gasto en **Offset account**: `606300`.
**Journal line**: Department `022`, CostCenter `009`.
**Main account 606300**: CostCenter **Fixed=`008`** en la sociedad del ejemplo.
**Voucher** inventado: `VCH-2026-001`; importe 1.000 unidades de moneda de contabilización.

### Asiento contable esperado, si todas las reglas validan
| Posted accounting entry (ejemplo) | Debit | Credit | Department | CostCenter |
|---|---:|---:|---|---|
| Expense / gasto `606300` | 1.000 | — | `022` | `008` (**Fixed**) |
| Vendor liability / cuenta AP | — | 1.000 | Depende de su configuración | Depende de su configuración |

No inventar la cuenta contable de AP: se determina por configuración de proveedor/perfil de contabilización. **No necesariamente se heredan las mismas dimensiones a ambos lados**.

### Ejercicio de troubleshooting
1. Verificar **Vendor Invoice Journal > Lines > Financial dimensions**; documentar el valor visible `009`.
2. Revisar **Main accounts > Legal entity overrides > Default dimensions** para cuenta 606300; confirmar que `CostCenter=008 (Fixed)` realmente aplica a la sociedad.
3. Revisar **Validate** y **Simulate posting** en un **sandbox** antes de contabilizar.
4. Una vez contabilizado, navegar a **General ledger > Inquiries and reports > Voucher transactions** y buscar voucher + fecha + sociedad.
5. Inspeccionar **Ledger account**, montos en débito/crédito, las dimensiones presentes y **Transaction origin / Original document** para rastrear origen.
6. Si en el asiento se ve CostCenter `009` en lugar de `008`, considerar que Fixed no está aplicado a la cuenta/sociedad correspondiente, se está observando otra cuenta, se confunde línea con asiento, o interviene una personalización. **No diagnosticar sin evidencia.**

## Tablas de F&O para empezar a programar

| Momento | Objeto | Qué investigar |
|---|---|---|
| Antes de contabilizar | `LedgerJournalTable` | Datos del encabezado del diario |
| Antes de contabilizar | `LedgerJournalTrans` | Líneas del diario |
| Después de contabilizar | `GeneralJournalEntry` | Encabezado del voucher / movimientos contables |
| Después de contabilizar | `GeneralJournalAccountEntry` | Líneas contables por cuenta, dimensiones e importes |
| Vinculación técnica | `GeneralJournalAccountEntry.GeneralJournalEntry` → `GeneralJournalEntry.RecId` | Relación técnica, no un join por texto de voucher |

La documentación Microsoft confirma las tablas de contabilidad y su vínculo:
- https://learn.microsoft.com/en-us/dynamics365/finance/finance-insights/tables-detail
- https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/sysadmin/archive-tables-reference
- https://learn.microsoft.com/en-us/troubleshoot/dynamics-365/finance/business-performance-analytics/missing-journal-entries-err00004

### X++ conceptual, solo lectura (no ejecutado)
```xpp
GeneralJournalEntry gje;
GeneralJournalAccountEntry gjae;

while select gje
    where gje.SubledgerVoucher == "VCH-2026-001"
    join gjae
        where gjae.GeneralJournalEntry == gje.RecId
{
    info(strFmt("Voucher: %1 | Amount: %2",
        gje.SubledgerVoucher,
        gjae.AccountingCurrencyAmount));
}
```
Ejemplo didáctico: un sistema real debe filtrar también entidad/ledger/fecha y respetar permisos. Para ver la dimensión legible no basta con imprimir `gjae.LedgerDimension` como número; esa referencia debe resolverse contra las tablas/objetos de dimensión. No conectar ni consultar SQL de producción directamente.

## Entrevista: respuesta breve
> I start with the journal line and check the default and fixed financial dimensions. After posting, I use the Voucher transactions inquiry to inspect the final ledger account, amounts, and dimensions. If necessary, I trace the transaction to its original document. On the technical side, I know that GeneralJournalEntry stores the journal entry header and GeneralJournalAccountEntry stores the corresponding ledger account entries.

## Glosario
- **Voucher transactions** — consulta de transacciones de asiento
- **Journal line** — línea de diario
- **Posted voucher** — comprobante contabilizado
- **Posted ledger entry** — movimiento contable contabilizado
- **Transaction origin** — origen de la transacción
- **Original document** — documento original
- **Ledger account** — cuenta contable + combinación de dimensiones
- **Accounting currency amount** — importe en moneda contable
- **Accounting entry** — movimiento contable / apunte contable
- **Troubleshooting** — diagnóstico de incidencias

## Estado de avance
Documentación y práctica **preparadas**, pendiente respuesta del alumno y operación real en ambiente cloud. No marcar como completado.
