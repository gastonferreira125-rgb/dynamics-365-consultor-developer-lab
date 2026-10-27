# DYN-01 — Práctica visual sin entorno ERP

**Fecha:** 27/10/2026. **Estado:** ejercicio de análisis a partir de imágenes reales; **no es ejecución de un sistema**.

## Objetivo
Aprender a interpretar la configuración de estructuras de cuentas y a planificar una verificación en el diario de facturas. Sin repetición de contabilidad básica, sin instalar ERP ni simular que se contabilizó nada.

## Pantalla 1: Account Structures

Captura oficial, procedente de [Microsoft Learn — Account structures overview](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/configure-account-structures).

![Estructura de cuentas de F&O — Microsoft Learn](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/media/account.png)

### Paso guiado
1. Leer la sección **Segments and allowed values**.
2. Localizar el bloque **Allowed value details**.
3. Verificar si está marcada la casilla **Blank values are allowed** en la condición seleccionada.
4. Identificar qué hace el operador para **CostCenter**, y qué rango de valores figura.
5. Distinguir la captura real (cuentas y valores de Microsoft) de nuestro caso didáctico (cuenta ficticia 610100/CostCenter 101/102).

### Mini-reto (sin respuesta automática)
En la captura oficial, ¿el valor vacío del segmento seleccionado está permitido o prohibido? ¿Bastaría observar ese dato para concluir la causa de un error en una factura? ¿Qué otra configuración habría que revisar?

**Concepto clave:** una estructura de cuentas define combinaciones permitidas. La aceptación o rechazo depende de todas las reglas aplicables, la cuenta utilizada, la compañía y posibles reglas avanzadas/fixed dimensions. No inventar el resultado de una transacción real.

## Pantalla 2: Vendor Invoice Journal

Referencia oficial con capturas y datos de ejemplo:
[Microsoft Learning MB-310 — Lab 3: Breakdown of voucher](https://microsoftlearning.github.io/MB-310-Microsoft-Dynamics-365-Finance/Instructions/Labs/LP3%20Lab%20-%20Breakdown%20of%20voucher.html)

- La guía navega a **Accounts payable > Invoices > Invoice journal**.
- En el ejemplo de Microsoft se crea un diario (Name `APInvoice`), se abren **Lines** y se trabaja con la cuenta de proveedor `US-111`. Estos datos son de ese laboratorio, **no** de nuestra factura ficticia.
- El alumno reconoce **New**, **Lines**, tipos de cuenta, importe y contrapartida.
- En el laboratorio adaptado al diagnóstico, antes de contabilizar se revisan dimensiones, estructura aplicable y, si el entorno lo permite, **Validate** y **Simulate posting**. La guía oficial de desglose incluye un paso **Post**, pero no debe ejecutarse sin entorno de pruebas y autorización.

## Evidencias a registrar tras cada clase
- Captura o enlace de referencia.
- Qué se identificó efectivamente.
- Hipótesis y su grado de verificación.
- Qué se haría en el entorno de pruebas.
- Limitaciones: **hoy no hay acceso a F&O**.

## Prioridad para conseguir entorno cloud
- Prueba F&O: [Microsoft Learn — Unified admin trials](https://learn.microsoft.com/en-us/power-platform/admin/unified-experience/admin-trials).
- Oferta condicionada a licencias/tenant/región; sin garantía para cuenta de Uruguay.
- Hasta obtenerla, trabajar en pantalla y laboratorio guiado, sin fingir operaciones.
- X++ con Visual Studio requiere un entorno de desarrollador diferente; el trial común no sirve.

[Trello DYN-01](https://trello.com/c/hVHlU4pU).


## Segunda interacción — respuesta sobre proveedor vs cuenta contable (27/10/2026)
El estudiante plantea revisar **ambas configuraciones** y **el origen de las dimensiones** antes de cambiar nada.

**Valoración:** correcta. Para completar el diagnóstico, investigar también:
1. Nombre de diario (**LedgerJournalName**) y encabezado (**LedgerJournalTable**).
2. Dimensiones de la cuenta de línea (proveedor) y valores que completan segmentos vacíos.
3. Cuenta de contrapartida (tipo Ledger): valores heredados de la cuenta de línea, y de la cuenta principal cuando haya vacíos.
4. Dimensiones fijas a nivel de cuenta principal/entidad legal: pueden sobrescribir el valor del asiento **durante la contabilización**, incluso si en pantalla aparece otro.
5. Account structure y advanced rules: comprobar que la combinación final sea válida.
6. Extensiones o integraciones, si es relevante.

**Documento técnico oficial:** https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/dimensions-default-values

**Métodos X++ de referencia mencionados por Microsoft:** `LedgerJournalEngine.accountModified()` y `LedgerJournalEngine.offsetAccountModified()` para dimension defaulting en diarios. No se ha abierto AOT ni ejecutado código.

**Siguiente desafío:** encabezado Department=022; proveedor Department=023 y CostCenter=009; contrapartida Ledger 606300 con CostCenter Fixed=008. Determinar valores visibles en línea y los del asiento final, distinguiendo fuente de valores y efecto de Fixed. Es un caso pedagógico con reglas de dimensión inventadas; verificar vigencia de account structures antes de considerar un resultado real.
