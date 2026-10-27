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


## Resolución del desafío de troubleshooting — 27/10/2026 (ES/EN)

**Pregunta:** el gasto de la cuenta principal \`606300\` aparece en **Voucher transactions** con \`CostCenter=009\`, pero esperábamos \`008\` porque supuestamente está configurada una dimensión fija.

**Respuesta (primera comprobación):** verificar el parámetro **Fixed value** del \`CostCenter\` para la **Main account 606300** en la **Legal entity** donde se hizo el asiento. No modificar el proveedor, la estructura ni el diario para intentar corregir un hecho que no se ha diagnosticado.

### Menús exactos

1. \`General ledger > Chart of accounts > Accounts > Main accounts\`.
2. Abrir \`606300\`, sección **Legal entity overrides**, seleccionar la sociedad del comprobante (p. ej. \`USMF\`) y pulsar **Default dimensions**.
3. Comprobar si \`CostCenter\` está en **Fixed value = 008** o **Not fixed**. No asumir que ver un valor \`008\` significa que su estado sea **Fixed**.
4. Para inspeccionar el asiento definitivo: \`General ledger > Inquiries and reports > Voucher transactions\`. Filtrar por sociedad, voucher, fecha y cuenta; abrir **Transaction origin** / **Original document** si es necesario.

### Interpretación

| Hallazgo real | Qué significa / siguiente acción |
|---|---|
| \`Not fixed\` o ningún override Fixed para esa sociedad | \`009\` podría ser el valor resultante de la línea, proveedor o diario; aclarar con Finanzas si la política contable realmente exige \`008\`. No cambiar sin autorización. |
| \`Fixed value = 008\` vigente al contabilizar | Bajo el flujo estándar de diarios financieros, el asiento de esa cuenta debería registrar \`008\`. Si muestra \`009\`, verificar que sea el **posted accounting entry** (y no la línea del diario), la cuenta/sociedad correctas y el alcance del voucher. |
| Fixed fue activado/cambiado **después** de contabilizar | La configuración actual no demuestra la configuración histórica; solicitar evidencias de cambios y no asumir que el asiento ya registrado cambió. |
| Configuración correcta, pero resultado discrepante | Investigar origen real de la transacción, reversas/reclasificaciones, **derived dimensions**, reglas avanzadas y personalizaciones/integraciones. Escalar con evidencia técnica. |

**Prueba segura en sandbox autorizado:** con la misma cuenta y sociedad, crear transacción **nueva** y comparar: (1) valor \`009\` en línea; (2) \`Validate\` y \`Simulate posting\` si el tipo de diario lo permite; (3) si procede y con autorización en test, ejecutar **Post** y confirmar \`008\` en Voucher transactions. Repetir prueba negativa y regresión para otras cuentas afectadas. Nunca actualizar asientos contabilizados mediante SQL.

**Cautela:** una estructura contable puede invalidar el resultado incluso con Fixed=008. El diagnóstico debe verificar **Account structure** y **Advanced rules**, pero solo después de comprobar el origen del valor incorrecto.

### Inglés para entrevista

> First, I verify whether the main account has a fixed financial dimension configured for the correct legal entity. Then I compare the journal line with the posted voucher. Fixed dimensions override entered values at posting time, so if the posted entry still shows a different cost center, I investigate the transaction origin, posting date, and any customizations before proposing a change.

### Conceptos nuevos

- **Main account** — cuenta principal
- **Legal entity override** — configuración específica por sociedad
- **Fixed value** — valor fijo; reemplaza durante posting
- **Not fixed** — valor no fijo; puede heredarse o cambiarse
- **Posting date** — fecha de contabilización
- **Journal line** — línea del diario, puede mostrar \`009\`
- **Posted accounting entry** — apunte contable definitivo, debería reflejar \`008\` si Fixed aplica
- **Transaction origin / Original document** — navegación al origen del asiento
- **Regression testing** — comprobar que el cambio no afecta procesos existentes

**Estado:** respuesta documentada con fuentes, **NO prueba ejecutada** porque seguimos sin sandbox F&O.

### Referencias oficiales

- [Default financial dimensions on financial journals](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/dimensions-default-values)
- [Financial dimensions and posting](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/Default-dimensions)
- [Default financial dimension values are incorrect](https://learn.microsoft.com/en-us/troubleshoot/dynamics-365/finance/general-ledger/incorrect-default-dimension-values)
- [View journal entries or transactions](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/tasks/view-journal-entries-or-transactions)
