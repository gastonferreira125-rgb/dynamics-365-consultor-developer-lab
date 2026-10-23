# DYN-01 — Matriz de pruebas UAT

Todas las pruebas pendientes hasta contar con entorno autorizado.

| ID | Escenario | Resultado esperado | Ejecutado |
|---|---|---|---|
| UAT-01 | Cuenta 610100 + CostCenter 101 | Combinación válida y asiento simulado correcto | No |
| UAT-02 | Cuenta 610100 + CostCenter 102 | Combinación válida si está autorizada para el gasto | No |
| UAT-03 | Cuenta 610100 + CostCenter vacío | Error si la regla exige valor | No |
| UAT-04 | Cuenta 610100 + CostCenter 999 | Error si está fuera de allowed values | No |
| UAT-05 | Proveedor/dimensión con valores por defecto | Verificar precedencia de valores en línea | No |
| UAT-06 | Cuenta con Fixed CostCenter | Simulación refleja política de dimensión fija | No |
| UAT-07 | Otro diario/otra cuenta afectada por estructura | No debe producirse regresión inesperada | No |
| UAT-08 | Misma estructura usada por otra legal entity | No romper reglas de otra sociedad | No |
| UAT-09 | Seguridad | Usuario autorizado puede corregir; no autorizado no | No |

## Criterios para aprobar
- Finanzas autoriza la imputación contable.
- Los asientos previstos tienen cuenta, signo, importe, moneda y dimensión correctos.
- Valores fuera de política siguen rechazados.
- Se registra resultado literal y fecha de ejecución en ambiente, sin datos sensibles.
- Si cambia una account structure, aplicar control de cambios y repetir pruebas de regresión.

**Importante:** `Validate` y `Simulate posting` no reemplazan la aprobación contable, ni demuestran por sí solas ausencia de impacto sobre otros documentos.
