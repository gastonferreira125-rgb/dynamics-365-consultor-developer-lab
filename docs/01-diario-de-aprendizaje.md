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
