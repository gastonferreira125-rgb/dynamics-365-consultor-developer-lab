# Conceptos técnicos específicos de Dynamics 365

## Finance & Operations (F&O)
- **Legal entity:** compañía bajo la cual se contabilizan transacciones.
- **Main account:** cuenta principal que integra una combinación contable.
- **Ledger dimension:** combinación validada de cuenta principal y dimensiones financieras.
- **Default dimensions:** dimensiones provenientes de valores por defecto en documentos, maestros o diarios; el origen y la precedencia dependen del escenario.
- **Fixed dimension:** configuración específica que puede reemplazar un valor al contabilizar; no es sinónimo de predeterminada.
- **Account structures:** segmentos, orden y valores admitidos para cuentas/dimensiones.
- **Advanced rules:** condiciones que exigen o restringen segmentos adicionales.
- **Validate / Simulate posting:** herramientas para verificar una transacción y prever contabilización, donde estén disponibles.
- **AOT:** Application Object Tree en un entorno de desarrollo con Visual Studio.
- **X++:** lenguaje de desarrollo de F&O, con consultas select/joins, tablas y clases.
- **Data entities / OData:** interfaces soportadas para integración; no autorizan actualizar SQL productivo.

Objetos a investigar con una instancia de desarrollo: `LedgerJournalTable`, `LedgerJournalTrans`, `DimensionAttributeValueCombination`. Son **candidatos**, no una atribución confirmada del error simulado.

## Business Central
- **Page Inspection:** ayuda a identificar los campos y objetos asociados a la página.
- **AL:** lenguaje de extensiones en Visual Studio Code.
- **Sandbox:** entorno no productivo donde se puede publicar/debuggear extensiones, si hay licencia y permisos.
- **Posting groups y dimensions:** configuración propia de BC, distinta de F&O.

## Regla profesional
No intentar solucionar errores contables mediante UPDATE en tablas de producción. Investigar en interfaz, reproducir, documentar, aplicar cambios autorizados y comprobar resultados.
