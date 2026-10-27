# DYN-01 — Default vs. Fixed dimensions (ES/EN) | Laboratorio guiado

Fecha: 27/10/2026. Estado: explicación teórica contrastada en documentación oficial. **Sin sandbox ni ejecución real**.

## Caso
| Origen | Department | CostCenter |
|---|---|---|
| Journal header | 022 | vacío |
| Vendor US-111 | 023 | 009 |
| Main account 606300 | sin default | 008, **Fixed** |

**Respuesta estándar esperada (sin derived dimensions ni personalizaciones):**
- **Journal line — Account (Vendor):** Department **022**, CostCenter **009**. El header aporta Department=022 y la cuenta del proveedor rellena solo el CostCenter que seguía vacío.
- **Journal line — Offset account (Ledger 606300):** Department **022**, CostCenter **009**. Primero copia las dimensiones de Account; la dimensión Fixed de la cuenta 606300 NO reemplaza un valor ya definido en la línea del diario.
- **Posted accounting entry para la cuenta 606300:** Department **022**, CostCenter **008**. Al realizar el posting, Fixed=008 sobrescribe el valor anterior. La línea del diario puede seguir mostrando 009; inspeccionar voucher y asientos contables.
- Se supone una combinación permitida. Si Account Structure/Advanced Rule invalida el resultado, **posting puede fallar**. Tampoco se determinó qué dimensiones llevaría el otro lado del asiento del proveedor, ya que no se proporcionó su cuenta principal y su posible configuración Fixed.

## Flujo de prioridades para un financial journal
1. **Journal name > journal header**: se copian default dimensions desde nombre a encabezado.
2. **Journal header > journal line Account**: se aplican primero las dimensiones del encabezado. Los campos vacíos se completan desde vendor/customer/ledger/etc.
3. **Journal line Account > journal line Offset account**: se copian primero las dimensiones de Account; si quedan blancos, se completan desde la cuenta de contrapartida.
4. **Posting**: se imponen **Fixed dimensions** de cada Main account en el accounting entry final, aunque el Journal line no las muestre.
5. **Validation**: account structures y advanced rules deben permitir la combinación contable final.

Importante: estas reglas se aplican a **financial journals** estándar; no extrapolar sin verificar a PO invoices, inventory journals y project journals. La documentación oficial distingue estos procesos.

## Rutas funcionales (interfaz en inglés)
| Qué inspeccionar | Ruta |
|---|---|
| **Journal name / default dimensions** | General ledger > Journal setup > Journal names > Financial dimensions |
| **Journal header** | Accounts payable > Invoices > Invoice journal > abrir diario > Financial dimensions |
| **Vendor master** | Accounts payable > Vendors > All vendors > seleccionar US-111 > Financial dimensions |
| **Main account / Fixed** | General ledger > Chart of accounts > Accounts > Main accounts > 606300 > Legal entity overrides > seleccionar sociedad > Default dimensions > CostCenter: Fixed value = 008 |
| **Account structures** | General ledger > Chart of accounts > Structures > Configure account structures |
| **Offset account dimensions** | Invoice journal > Lines > Financial dimensions > Offset account |
| **Posted voucher** | En diario > Lines > Voucher, u opción de Voucher transactions disponible en la experiencia del usuario |

No cambiar configuración en producción para demostrar conceptos.

## Glosario técnico ES/EN
- **Financial dimension** = dimensión financiera
- **Default dimension** = dimensión predeterminada
- **Fixed dimension / Fixed value** = dimensión fija / valor fijo
- **Journal name** = nombre de diario (tipo de diario)
- **Journal header** = encabezado del diario
- **Journal line** = línea del diario
- **Vendor master data** = maestro de proveedores
- **Main account** = cuenta principal
- **Offset account** = cuenta de contrapartida
- **Ledger** = libro mayor / tipo de cuenta contable
- **Account structure** = estructura contable
- **Advanced rules** = reglas avanzadas
- **Posting** = contabilización
- **Posted voucher** = comprobante contabilizado
- **Troubleshooting** = investigación y resolución de incidencias
- **Dimension defaulting** = asignación automática de dimensiones
- **Legal entity overrides** = parámetros por sociedad para la cuenta principal

## Frase útil en entrevista
> When troubleshooting financial dimension issues in Dynamics 365 Finance, I first check the journal header, the vendor's default dimensions, and the offset account. Then I review the main account configuration and the active account structure. A fixed dimension can override a value during posting, even when the journal line displays a different value. I validate the expected posting and test the change in a sandbox before recommending any production update.

Traducción: para diagnosticar dimensiones reviso el encabezado, las dimensiones del proveedor y la cuenta de contrapartida; después la configuración de la cuenta principal y la estructura activa; una dimensión fija puede reemplazar un valor al contabilizar, por lo que valido el asiento previsto y pruebo en sandbox antes de recomendar cambios productivos.

## Próximo ejercicio práctico
Abrir captura de **Main accounts > Legal entity overrides > Default dimensions** e identificar **Fixed value** versus **Not fixed**; luego contrastar con **Journal line** y **Posted voucher** en Microsoft Learn. Pendiente de sandbox cloud.

## Fuentes oficiales
- https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/dimensions-default-values
- https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/default-dimensions
- https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/financial/dimension-defaulting
- https://learn.microsoft.com/en-us/dynamics365/finance/general-ledger/configure-account-structures
- https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/vendor-invoices-overview
