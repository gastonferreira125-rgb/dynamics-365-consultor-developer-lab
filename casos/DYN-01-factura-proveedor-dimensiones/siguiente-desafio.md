# Próximo desafío — Investigar el origen de una dimensión

Caso: el usuario afirma que el proveedor tiene Centro de costos `101`, pero la línea del diario exhibe valor vacío. Antes de modificar nada:

1. Verificar **dónde** está definido el 101 (proveedor, encabezado, plantilla, cuenta, otro documento).
2. Identificar si la línea proviene de un diario de facturas, factura de compra o proceso integrado.
3. Revisar precedencia de dimensiones por defecto y si el dato se copió al crear la línea.
4. Examinar estructura contable, reglas avanzadas y dimensiones fijas.
5. En entorno de prueba recrear documento equivalente, comparar línea y asiento simulado.
6. Documentar qué cambió y por qué, y comprobar regresión en otros documentos.

## Hito técnico
Explorar (en ambiente de desarrollo adecuado) los objetos `LedgerJournalTable`, `LedgerJournalTrans`, `DimensionAttributeValueCombination`. Confirmar relaciones y campos reales antes de usar código X++; no modificar SQL productivo.

Enlace: [Microsoft Learn — dimensiones predeterminadas en diarios](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/dimensions-default-values).
