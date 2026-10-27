# DYN-02 — Laboratorio ejecutable: Voucher, JOIN y dimensiones (SQL/Python)

**Fecha:** 27/10/2026. **Producto de referencia:** Dynamics 365 Finance & Operations. **Estado:** código de demostración ejecutado y probado con cinco pruebas automáticas en un ambiente Python/SQLite. **No** es ejecución sobre Dynamics 365 ni sobre un entorno X++.

## Objetivo

Aprender a unir `GeneralJournalEntry` con `GeneralJournalAccountEntry`, filtrar por empresa y voucher, comprobar que los movimientos cuadren y detectar una discrepancia de `Fixed dimension`. También ejercitar términos profesionales en inglés.

## Opción recomendada si ya tenés Visual Studio instalado (sin Codespaces)

**No hace falta Codespaces ni Docker.** Este laboratorio es solo un script de Python con SQLite (incluido en Python); no incluye servidor F&O ni SQL Server. Si Python 3 ya está instalado, abrí la carpeta clonada/descargada del repositorio en Visual Studio, Visual Studio Code o una terminal Windows y ejecutá desde la raíz:

```powershell
py -3 labs/DYN-02-vouchers-cloud/lab.py
py -3 labs/DYN-02-vouchers-cloud/lab.py --company USMF --voucher VCH-2026-002
py -3 -m unittest discover -s labs/DYN-02-vouchers-cloud -v
```

En sistemas donde `py` no esté disponible, probá `python` o `python3`, si el intérprete existe. En **Visual Studio** (no Visual Studio Code), para trabajar con archivos Python en el IDE pueden requerirse la carga de trabajo *Python development* y el intérprete, por separado; no instalar estas herramientas si no son necesarias. Como alternativa, ejecutar desde la terminal Windows abierta en la carpeta del proyecto. Si Python **no** está instalado, no lo presupongas ni descargues software sin consentimiento: hay alternativa de usar C# en su instalación actual.

**Distinción:** este ejercicio simula tablas con SQLite. Para ejecutar **X++ verdadero**, Microsoft documenta *Unified developer experience*: Visual Studio puede editar/compilar en la PC y ejecutar/desplegar en un runtime F&O cloud, pero requiere herramientas de desarrollo, metadatos y un entorno F&O autorizado; Visual Studio por sí solo no basta. https://learn.microsoft.com/en-us/power-platform/developer/unified-experience/finance-operations-debug

## Alternativa: ejecutar en navegador (GitHub Codespaces)

1. Abrir el [repositorio principal](https://github.com/gastonferreira125-rgb/dynamics-365-consultor-developer-lab).
2. Presionar **Code > Codespaces > Create codespace on main**. Seleccionar la máquina de menor tamaño si ofrece elección. El equipo ejecuta en **la nube**, no en tu PC.
3. En la terminal integrada de VS Code web, pegar:

   ```bash
   python3 labs/DYN-02-vouchers-cloud/lab.py
   ```

4. Comparar otro comprobante:

   ```bash
   python3 labs/DYN-02-vouchers-cloud/lab.py --voucher VCH-2026-002 --company USMF
   ```

5. Ejecutar los tests automáticos:

   ```bash
   python3 -m unittest discover -s labs/DYN-02-vouchers-cloud -v
   ```

6. Al salir, **Stop codespace** en GitHub (y borrar el codespace cuando ya no lo necesites) para evitar seguir consumiendo cuota.

GitHub Codespaces para cuentas personales ofrece una cuota de uso mensual incluida; consulta el consumo y evita habilitar facturación automática si solo querés la parte gratuita: https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-included-usage .

**Si no tenés Codespaces disponible**, podemos ejecutar y explicar el mismo código acá y usar `github.dev` para editarlo online, pero `github.dev` NO ejecuta Python ni tiene terminal.

## Qué ocurre en nuestros datos FICTICIOS

- Voucher `VCH-2026-001` de `USMF`: gasto `606300` con Department `022`, CostCenter `008` y cargo 1.000; AP `201100` con abono -1.000. **Cuadra**.
- Voucher `VCH-2026-002` de `USMF`: cuenta `606300` registra CostCenter `009` cuando en nuestra tabla ficticia de reglas fijas figura `008`. El programa lo marca como **anomalía deliberada**.
- Voucher `VCH-2026-001` también existe en `DEMF` con `RecId` distinto. **Por eso filtrar solo por texto de Voucher no alcanza**.

Las tablas ficticias `JournalLineExample`, `FixedDimensionExample` y el campo `Company` son ayudas didácticas. **En F&O real no hay columnas planas CostCenter, Department y MainAccount en GeneralJournalAccountEntry como en nuestro SQLite**: la combinación contable está normalizada/referenciada mediante `LedgerDimension` y el libro/sociedad deben obtenerse con las relaciones y APIs reales. No ejecutar este SQL contra bases reales de F&O.

La unión entre `GeneralJournalAccountEntry.GeneralJournalEntry` y `GeneralJournalEntry.RecId` sí está documentada por Microsoft: https://learn.microsoft.com/en-us/troubleshoot/dynamics-365/finance/business-performance-analytics/missing-journal-entries-err00004 .

## SQL vs X++

```sql
SELECT gje.SubledgerVoucher, gjae.AccountingCurrencyAmount
FROM GeneralJournalEntry gje
JOIN GeneralJournalAccountEntry gjae
  ON gjae.GeneralJournalEntry = gje.RecId;
```

```xpp
GeneralJournalEntry gje;
GeneralJournalAccountEntry gjae;
while select gje
    where gje.SubledgerVoucher == "VCH-2026-001"
    join gjae
        where gjae.GeneralJournalEntry == gje.RecId
{
    info(strFmt("%1", gjae.AccountingCurrencyAmount));
}
```

X++: **ejemplo de lectura**, todavía no compilado ni validado en AOT. En un desarrollo real faltan filtros por libro, sociedad y fecha; no usar esta consulta como un reporte de producción.

## Mini ejercicio

1. Ejecutá voucher `001` y mirá el importe neto.
2. Ejecutá voucher `002` y explicá por qué una alerta de Fixed dimension **no prueba por sí sola** un error histórico.
3. Abrí [consulta.sql](consulta.sql), identificá `INNER JOIN`, `ON` y `WHERE`.
4. Ejecutá `python3 -m unittest discover -s labs/DYN-02-vouchers-cloud -v`; buscá **Ran 5 tests ... OK**.

**Vocabulario para entrevista:** record identifier (`RecId`), join, foreign key, posted journal entry, account entry, accounting currency amount, cost center, reconciliation, troubleshooting, fixed dimension.

**Trello:** [DYN-01](https://trello.com/c/hVHlU4pU) y [DYN-05](https://trello.com/c/xh0EHjNa).
