# ENV-01 — Registro de Business Central bloqueado en Uruguay

**Fecha:** 27 de octubre de 2026.
**Estado:** bloqueo confirmado de **registro autoservicio**, no del producto completo ni del entorno de pruebas proporcionado por partners.

## Evidencia observada
Al abrir el enlace de registro a Sandbox Business Central desde `signup.microsoft.com`, antes del paso "Crear una cuenta" aparece: **"Dynamics 365 Business Central no está disponible en este mercado"**.
Captura aportada por el alumno al chat. **No se sube al repositorio por tratarse de una captura privada del navegador.**

## Causa y alcance contrastados
- Microsoft [lista a Uruguay como **Available**, con localización **Partner** y base **W1**](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/compliance/apptest-countries-and-translations).
- Para países con localización partner, [Microsoft establece una ruta diferente para la prueba](https://learn.microsoft.com/es-es/dynamics365/business-central/trial-signup): el partner asigna la SKU de trial en CSP al tenant cliente, configura localización y datos de muestra y comparte el enlace de acceso.
- Según Microsoft, usar la prueba creada por un partner **no obliga a adquirir licencias** de ese partner.
- Microsoft Learn provee [guías prácticas MB-800](https://microsoftlearning.github.io/MB-800-Business-Central-Functional-Consultant/), pero las instrucciones por sí mismas **no crean ni conceden una instancia real**.
- Se puede recorrer una [visita guiada oficial interactiva](https://guidedtour.microsoft.com/en-us/guidedtour/dynamics/business-central). **No** es un ERP configurable ni un entorno para publicar código.

## Próximos pasos
1. Solicitar a un partner que habilite una **Business Central Trial** en un tenant y confirme si se puede crear un **sandbox online con permisos de publicación de extensiones AL**. Usar [directorio oficial de partners Microsoft](https://www.microsoft.com/es/dynamics-365/partners/find-a-partner).
2. En paralelo, validar si el PC tiene Windows compatible, virtualización/containers, RAM y espacio para ejecutar un **sandbox local** con [Docker Windows + BCContainerHelper](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-get-started-container-sandbox). El sandbox local está documentado como **gratis localmente**, pero Docker Desktop u otros componentes pueden tener licencias según el caso. **No instalar antes de comprobar requisitos**.
3. Mientras se obtiene acceso, explorar [Microsoft Business Central Guided Tour](https://guidedtour.microsoft.com/en-us/guidedtour/dynamics/business-central) y trabajar con capturas y guías del proveedor (sin marcar como operaciones realizadas).
4. Mantener aparte la búsqueda de un trial Dynamics 365 **Finance**, ya que es un producto diferente.

## Nota para soporte
No recomendamos alterar artificialmente el país de facturación, usar ubicaciones falsas ni instalar paquetes no oficiales como solución al bloqueo.

**Trello:** [ENV-01](https://trello.com/c/6NFDf0SZ) y [DYN-01](https://trello.com/c/hVHlU4pU).

**Pendientes de evidencia:** nombre del partner, invitación real al tenant, entrada efectiva a BC, sandbox visible, publicación AL de prueba.
