# ENV-01 — Evaluación del equipo para sandbox local Business Central

**Fecha:** 27/10/2026. **Evidencia:** captura de Windows > Sistema > Información compartida en el chat. No se incluye la captura ni identificadores del dispositivo por privacidad.

## Especificaciones visibles

| Recurso | Observado | Evaluación |
|---|---|---|
| Modelo | MSI Summit E13 AI Evo | Portátil x64 |
| CPU | Intel Core Ultra 7 155H | Suficiente para laboratorio de desarrollo |
| RAM | 16 GB | Justa para Docker, BC, SQL y VS Code en simultáneo |
| Almacenamiento total | 954 GB | Amplio |
| Almacenamiento usado | 238 GB | Espacio libre amplio |
| GPU | Intel Arc integrada | No es un limitante material para AL |
| Windows Edition | No visible | **Pendiente: comprobar si es Pro/Enterprise** |
| Virtualización | No visible | **Pendiente: comprobar BIOS/UEFI y características Windows** |

## Verificación pendiente antes de instalar

1. Abrir **Configuración > Sistema > Información > Especificaciones de Windows** y registrar **Edición** y **Versión** (sin product ID).
2. Abrir **Administrador de tareas > Rendimiento > CPU** y observar **Virtualización: habilitada/deshabilitada**.
3. En Windows 11 Pro/Enterprise, revisar disponibilidad de **Hyper-V** y **Containers** y derechos de administrador. No activar todavía.
4. Confirmar RAM realmente disponible sin apps pesadas: 16 GB es una configuración justa, evitar múltiples contenedores.
5. Confirmar si se admite/conviene instalar Docker Desktop en este contexto de licencia. Docker Desktop Windows requiere instalación **all-users** para usar Windows containers.
6. Solo entonces instalar Docker, activar Windows containers y BCContainerHelper si procede.

## Razonamiento basado en fuentes oficiales
- [Microsoft Learn — Running a container-based development environment](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-get-started-container-sandbox): contenedor BC puede consumir al menos 6 GB RAM y artifacts/imágenes unos 15 GB. Requiere Docker configurado con **Windows containers**.
- [Docker Desktop para Windows — requisitos](https://docs.docker.com/desktop/setup/install/windows-install/): Windows containers requieren Windows Pro/Enterprise y una instalación de Docker Desktop que admita Windows containers; Home no es una solución por WSL/Linux containers.
- [Business Central 2026 wave 2 system requirements](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/deployment/system-requirements-business-central-v29): 16 GB como referencia para desarrollo y despliegue de pequeñas extensiones; más RAM para desarrollos grandes.
- [BC sandbox overview](https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/developer/devenv-sandbox-overview): sandbox local gratuito en infraestructura local, licencias de herramientas y condiciones separadas.

**Resultado:** equipo con CPU y disco aptos, RAM **ajustada pero no descartada**; edición Windows y virtualización aún sin verificar. **No se instaló Docker ni se creó sandbox.**

## Plan alternativo
Si Windows es Home o el rendimiento resulta insuficiente, solicitar BC sandbox al partner mediante Trial/CSP. Mientras tanto, desarrollar sintaxis y proyectos AL sin afirmar publicación ni ejecución.
