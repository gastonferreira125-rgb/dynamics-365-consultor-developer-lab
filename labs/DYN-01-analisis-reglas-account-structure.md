# DYN-01 — Lectura aplicada de Account Structures (Manufacturing P&L)

**Fuente de la captura:** [Microsoft Learn — Account structures](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/media/account.png).

**Fecha de la clase:** 27/10/2026. **Modalidad:** captura oficial; sin acceso a ERP real. **Estado:** ejercicio abierto.

## Valores visibles en la pantalla

| MainAccount | BusinessUnit | Department | CostCenter | ItemGroup |
|---|---|---|---|---|
| 400000..999999 | `"";*` | `"";022` | `"";007..008` | `"";*` |
| 400000..999999 | `"";*` | `023` | `"";009..012` | `"";*` |
| 400000..999999 | `"";*` | `024` | `"";013..014` | `"";*` |
| 400000..999999 | `"";*` | `025..034` | `"";007..014` | `"";*` |

**Observaciones importantes**
- `""`: se permite vacío; `*`: cualquier valor no vacío; `"";*`: vacío o cualquiera.
- En la primera fila, `"";007..008` permite Centro de costos vacío, `007` o `008`.
- La casilla **Blank values are allowed** está marcada para el segmento seleccionado **CostCenter**, en la primera fila.
- Reglas de una fila forman una combinación; p. ej. en primera fila Department `022` y CostCenter `009` no son compatibles.
- No inferir que toda la estructura permite cualquier valor o que todos los valores vacíos son válidos en cualquier compañía.
- No confundir los datos de la captura oficial con el caso ficticio de cuenta `610100`, centros `101/102`.

## Práctica (razonamiento, NO simulación ejecutada)

Suponer MainAccount `610100`, BusinessUnit `001`, ItemGroup vacío.

| Caso | Department | CostCenter | Resultado esperado **según filas visibles**, sin reglas avanzadas |
|---|---|---|---|
| A | `022` | `008` | Válido |
| B | `022` | `009` | Inválido |
| C | `023` | `009` | Válido |
| D | `023` | vacío | Válido |

**Desafío:** si el departamento real es 022 y el centro propuesto es 009, ¿cómo lo investigarías antes de editar una regla? Revisar estructura activa por sociedad, origen de dimensiones, dueño del dato y autorización financiera. Probar positivo, negativo y regresión en sandbox autorizado.

Referencias: [Account structures overview](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/configure-account-structures) y [Crear/activar estructuras](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/tasks/create-account-structures).

**Pendiente de registrar:** interpretación y propuesta del estudiante, evidencias y cierre real.

## Resolución del estudiante — 27/10/2026
**Respuesta:** «En este caso, agregar esa combinación a la configuración».

**Devolución del instructor:** técnicamente correcta SI Finanzas valida que Department 022 / CostCenter 009 debe estar permitido. Una edición posible sería pasar de `"";007..008` a `"";007..009` en la rama correspondiente, pero eso amplía la autorización a todas las cuentas y unidades de negocio cubiertas por la rama, no solo a la factura o a la cuenta 610100.

**Lección técnica:** las account structures son árboles presentados como filas. Los nodos padres (ej., rango de MainAccount) pueden compartirse y modificar sus criterios afecta a varias filas. Para acotar a una cuenta, diseñar criterios específicos con precaución para no crear rutas que se superpongan; controlar uso por otras entidades legales y reglas avanzadas.

**Procedimiento en sandbox autorizado:**
1. Confirmar requerimiento y alcance (cuenta, departamentos, centros y sociedades) con Finanzas.
2. General ledger > Chart of accounts > Structures > Configure account structures > Edit, para crear una versión borrador.
3. Modificar el criterio aprobado, evitando solapamientos.
4. Ejecutar Validate; comprobar superposiciones potenciales adicionales antes y durante Activate.
5. Activar exclusivamente en sandbox; la activación sincroniza transacciones **no contabilizadas** y puede tardar según volumen.
6. UAT: cuenta/departamento autorizados con 009 acepta; 007/008 siguen aceptados; 010 sigue rechazado; otra cuenta no adquiere permiso involuntariamente; revisar efecto en otras sociedades.
7. Documentar cambio y aprobación antes de considerar producción.

**Estado:** respuesta conceptual evaluada; **NO hubo edición, activación, contabilización ni prueba en F&O real**.

**Fuentes:** [Overview account structures](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/configure-account-structures), [Create/activate/modify](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/tasks/create-account-structures) y [Configure ledgers](https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/configure-ledger).
