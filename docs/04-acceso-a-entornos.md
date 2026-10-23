# Cómo conseguir un entorno de práctica de Dynamics 365

**Situación al 23/10/2026:** sin acceso confirmado a un entorno de F&O o BC. **No se ha iniciado ninguna prueba ni se ha desplegado software en la cuenta del estudiante.**

## A. Business Central — funcional + desarrollo AL
1. Comenzar por la [prueba oficial de Business Central](https://learn.microsoft.com/en-us/dynamics365/business-central/trial-signup).
2. La inscripción requiere **correo profesional o educativo** y tenant Microsoft 365, no Gmail/Hotmail personal: [Trial FAQ](https://learn.microsoft.com/en-us/dynamics365/business-central/trial-faq).
3. Uruguay está disponible con localización provista por **partner** y base W1, según [lista oficial](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/compliance/apptest-countries-and-translations). Dependiendo de la oferta y configuración, podría requerirse gestión con partner para la prueba localizada.
4. Para programar: [Get started with AL](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-get-started). Se requiere sandbox online, Visual Studio Code y extensión AL.
5. En VS Code: `AL: Go!`, seleccionar cloud sandbox, autenticar y probar HelloWorld con `Ctrl+F5`. Confirmar permisos de publicación.

**No presuponer que un trial estándar garantiza sandbox con permisos de desarrollo.** Revisar acceso real y políticas del tenant.

## B. Dynamics 365 Finance — funcional
1. Microsoft documenta pruebas gratuitas F&O de 30 días (escenarios preconfigurados): [Before you buy](https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/fin-ops/get-started/before-you-buy).
2. Para prueba administrativa moderna: administrador de tenant entra a [Microsoft 365 Admin Center](https://admin.microsoft.com/) > Marketplace, busca prueba gratuita de Finance y asigna la licencia.
3. Luego [Power Platform Admin Center](https://admin.powerplatform.microsoft.com/) > Manage > Environments > New > Trial (subscription-based) > Enable Dynamics 365 apps > plantilla Finance (si está disponible en tenant y región).
4. Revisar entorno y permisos asignados antes de una práctica de configuración.
5. La prueba estándar no admite Visual Studio/X++: se necesita sandbox orientado a desarrollo. [Documentación oficial](https://learn.microsoft.com/en-us/power-platform/admin/unified-experience/admin-trials).

## Evidencia de acceso a registrar
- [ ] Correo usado es profesional/educativo; sin almacenar dirección ni contraseñas en el repo.
- [ ] Producto (Finance/BC), tipo de entorno y vencimiento.
- [ ] Permisos y empresa de demo visibles.
- [ ] Pantalla inicial (ocultar datos sensibles).
- [ ] Primer laboratorio ejecutado.
