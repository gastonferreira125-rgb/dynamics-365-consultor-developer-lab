# DYN-01: diagnóstico de factura proveedor con dimensión obligatoria

**Simulación didáctica, NO incidencia real.**
- Compañía USMF (si existe), proveedor V-1001, factura INV-2026-158.
- Gasto: cuenta 610100, departamento FIN, centro de costos vacío.
- Supuesto: estructura contable exige Centro de costos 101 o 102.
- Síntoma supuesto: combinación contable inválida al validar una factura por diario.

## Hipótesis a contrastar
1. Segmento vacío no permitido en estructura activa.
2. Dimensión predeterminada no heredada como esperaba el usuario.
3. Regla avanzada restringe combinación o exige dimensión adicional.
4. Dimensión fija altera el valor al contabilizar.
5. Cuenta/entidad legal o maestro contable configurado de otra forma.

## Diagnóstico propuesto
1. Pedir número, usuario, sociedad, fecha, pantalla, mensaje exacto y paso que falla.
2. Verificar flujo: factura desde diario o desde orden de compra; no son idénticos.
3. Revisar líneas y dimensiones disponibles en el documento aún no contabilizado.
4. Consultar estructura contable activa y restricciones por cuenta y compañía.
5. Preguntar a Finanzas qué centro corresponde, sin inventar valor para pasar la validación.
6. Priorizar completar dato de línea con permisos, si era obligatorio, antes de relajar reglas globales.
7. Si se requiere cambiar configuración, evaluar otras cuentas/sociedades, seguridad, cambios y aprobación.
8. Ejecutar Validate y Simulate posting en entorno habilitado y no productivo.
9. Registrar resultado, aprobar UAT y **solo entonces** seguir el proceso formal de contabilización.

**Respuesta del estudiante:** explicó correctamente la necesidad de revisar documentos pendientes y validez de la configuración, y planteó alta de dimensión o excepción solo tras relevamiento. Identificó como área a aprender cómo probar que la solución es segura.

**Resultado pendiente:** ninguna ejecución real. Ver [matriz UAT](pruebas-uat.md) y [laboratorio visual](../../labs/DYN-01-laboratorio-visual-factura-proveedor.md).
