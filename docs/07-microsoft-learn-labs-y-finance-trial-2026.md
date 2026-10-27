# ENV-02 — Microsoft Learn, laboratorios F&O y alternativas cloud (octubre 2026)

**Fecha de verificación:** 27/10/2026. **Política del estudiante:** NO instalar entornos F&O/Business Central ni Docker en su PC. Se priorizan laboratorios accesibles desde navegador o nube provista por Microsoft/partner.

## ¿Microsoft Learn incluye laboratorios en cada lección?
**No.** Las rutas mezclan contenido explicativo, ejercicios que se pueden hacer sin ERP, comprobaciones de conocimientos y ejercicios que necesitan ambiente. Un ejercicio descrito como "hands-on" no implica que Learn provea la máquina virtual.

## VM de Finance & Operations en Microsoft Learn: estado documentado
- Hasta junio de 2026 algunos ejercicios de MB-310/MB-500 ofrecían un botón **Launch VM / Launch Lab**, desaparecido para varios usuarios entre 25–30 de junio de 2026.
- En consulta de **6–10 de julio de 2026** un colaborador de Microsoft Q&A indicó que las **VM de laboratorio de F&O no estaban disponibles**, sin fecha prevista de resolución: https://learn.microsoft.com/en-us/answers/questions/5939196/why-isnt-an-vm-popping-up-on-this-website-https-le
- El **14 de septiembre de 2026**, en MB-310 otros usuarios seguían sin **Launch VM**; se aclaró que las instrucciones de laboratorios no incluyen ambiente hospedado y que se debe acceder por separado a F&O, a veces vía instructor/partner: https://learn.microsoft.com/en-us/answers/questions/6003022/no-longer-see-option-to-access-lab-launch-vm-on-mb
- No hay confirmación pública comprobada de restablecimiento general al 27/10/2026. No afirmar retirada definitiva.

## Hay guías de laboratorio oficiales MB-310, pero SIN instancia ERP incluida
- Índice de los cinco laboratorios: https://microsoftlearning.github.io/MB-310-Microsoft-Dynamics-365-Finance/
- Ejemplo de AP/journal/voucher con capturas auténticas: https://microsoftlearning.github.io/MB-310-Microsoft-Dynamics-365-Finance/Instructions/Labs/LP3%20Lab%20-%20Breakdown%20of%20voucher.html

## ¿Hay prueba gratuita de Finance?
**Documentación de Microsoft: sí, condicionada por acceso/elegibilidad y ruta de provisión.**
- La página técnica "Before you buy" habla de exploración 30 días con datos de prueba y funcionalidades limitadas: https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/fin-ops/get-started/before-you-buy
- El procedimiento más explícito se encuentra en "Unified admin trials": el administrador de tenant busca una licencia **Finance trial** en Marketplace de Microsoft 365, se la asigna, y crea un entorno **Trial (subscription-based)** en el Power Platform Admin Center habilitando apps Dynamics y plantilla Finance si aparece: https://learn.microsoft.com/en-us/power-platform/admin/unified-experience/admin-trials
- Restricción **importante**: las pruebas F&O estándar NO permiten desarrollo X++ con Visual Studio: se requiere un **sandbox de desarrollo distinto**.
- Hay desajuste en interfaces actuales: catálogo comercial global de pruebas Dynamics 365 muestra en Finance **Request a demo**, no **Try for free**: https://www.microsoft.com/en/dynamics-365/free-trial . Por eso, no garantizar auto-registro disponible en Uruguay ni para cuentas sin tenant admin.

## Ruta de decisión del estudiante
1. Comprobar acceso de administrador al Microsoft 365 Admin Center en un tenant profesional autorizado, sin datos de credenciales compartidos en el chat.
2. Buscar si aparece "Dynamics 365 Finance" con prueba gratuita en Marketplace. Si no aparece, NO prometerlo; consultar a Microsoft/partner por trial o demo interactiva.
3. Si obtiene trial Finance, entrar al ambiente únicamente desde navegador y realizar laboratorio DYN-01 de AP/GL: no ejecutar producción ni personalizaciones.
4. Para X++ solicitar laboratorio hospedado con desarrollador a proveedor educativo/partner, no instalar VM local.
5. Si no hay trial, usar guías oficiales MB-310 con capturas de pantallas, casos guiados en el chat sin reportarlos como ejecución real.

**Estado:** sin ambiente provisionado; acceso a labs Learn no confirmado; ruta cloud en investigación.
