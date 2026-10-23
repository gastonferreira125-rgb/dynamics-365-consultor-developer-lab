# Ejercicio 02 — Default dimension vs. Fixed dimension

## Escenario ficticio
Una factura de proveedor lleva un gasto a la cuenta `610100`. El encabezado del diario contiene Centro de costos `102`, el proveedor tiene predeterminado `101`, pero la cuenta tiene un Centro de costos marcado **Fixed = 103**.

Finanzas afirma que el gasto debe imputarse al centro `101`.

## Lo que se investiga
No confiar únicamente en la dimensión visible en la línea. Según la configuración y las reglas de precedencia, una dimensión fija puede imponerse al contabilizar. Verificar **simulación de asientos** y configuración de la cuenta principal.

Guía de Microsoft: [Default financial dimensions on financial journals](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/dimensions-default-values).

## Desafío
1. ¿Qué dimensión puede mostrarse en la línea del diario?
2. ¿Cuál podría usarse en el asiento final y por qué?
3. ¿Es correcto editar encabezado, línea o Fixed dimension si Finanzas requiere 101?
4. ¿Qué alcance tendría el cambio de una dimensión fija para otras transacciones?
5. ¿Qué pruebas UAT realizarías para evitar regresiones?

## Criterio
No cambiar una dimensión fija global para resolver una sola factura sin análisis de otras cuentas/compañías/transacciones y aprobación formal. La respuesta depende de configuración observada; no hay ejecución real.

**Estado:** pendiente de resolución guiada en entorno demo.
