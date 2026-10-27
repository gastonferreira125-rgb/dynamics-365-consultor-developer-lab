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
