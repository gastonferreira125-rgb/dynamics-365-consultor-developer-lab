# DYN-01 — Laboratorio visual de F&O: factura de proveedor

**Estado:** preparado, sin ejecución real en un entorno F&O. **Control:** [Trello DYN-01](https://trello.com/c/hVHlU4pU).
Objetivo: reconocer y ejecutar en sandbox los pasos de diagnóstico de una factura que falla por dimensiones financieras.

## Pantalla A: diario de facturas de proveedor
Ruta habitual: **Accounts payable > Invoices > Invoice journal**.
Referencia visual real: [Laboratorio Microsoft Learning MB-310 con capturas](https://microsoftlearning.github.io/MB-310-Microsoft-Dynamics-365-Finance/Instructions/Labs/LP3%20Lab%20-%20Breakdown%20of%20voucher.html).
Guía funcional Microsoft: [Record vendor invoice in the invoice journal](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/tasks/record-vendor-invoice-invoice-journal).

### Ejercicio guiado cuando haya entorno
1. Identificar compañía activa y permisos; elegir **USMF** solo si existe.
2. Entrar al diario, revisar encabezado, estado, nombre del diario y líneas. No publicar ni contabilizar.
3. Encontrar tipo de cuenta, proveedor, cuenta de contrapartida y **Financial dimensions**.
4. Buscar acción **Validate** y **Simulate posting** (la ubicación exacta depende de versión/rol).
5. Ejecutar únicamente en demo/sandbox autorizado. Registrar mensajes literales y asientos previstos.
6. Distinguir errores de combinación contable de validaciones de proveedor, período y diario.

## Pantalla B: estructuras contables
Ruta habitual: **General ledger > Chart of accounts > Structures > Configure account structures**.
Referencia visual: [Account structures](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/configure-account-structures).

### Ejercicio guiado
1. Identificar la estructura activa que aplica a la cuenta del gasto y compañía.
2. Revisar **Segments and allowed values**.
3. Para Centro de costos, inspeccionar **Allowed value details**; distinguir cualquier valor, rango, específicos y blanco.
4. Revisar reglas avanzadas y configuraciones de dimensiones fijas en la cuenta.
5. **No editar ni activar** estructuras sin evaluación de impacto.

## Caso ficticio que usaremos
Compañía `USMF`; proveedor `V-1001`; factura `INV-2026-158`; cuenta de gasto `610100`; departamento `FIN`; centro de costos vacío. La estructura hipotética permite `101` y `102`.

**Resultado esperado del laboratorio:** indicar dónde nació el valor vacío, por qué la combinación se bloqueó, cómo corregir la transacción no contabilizada sin abrir reglas globales y qué pruebas evidencian seguridad.

## Evidencias por completar
- [ ] Captura real de diario en sandbox (con datos sensibles ocultos).
- [ ] Mensaje real y explicación de origen.
- [ ] Captura de estructura aplicable.
- [ ] Resultado de Validate y Simulate posting.
- [ ] Decisión autorizada y regresión documentada.

**Mientras no haya acceso:** solo aprendizaje con capturas del fabricante; no declarar prueba real.
