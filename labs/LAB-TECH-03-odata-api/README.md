# LAB-TECH-03 — Consumir una API OData con C# (antes de integrar Dynamics 365 Finance)

**Inicio:** 02/11/2026. **Estado:** guía publicada; **no se ejecutó todavía**. **Modalidad:** navegador + Visual Studio existente. No Docker, no servidor ERP y no nuevos paquetes de terceros.

## Objetivo profesional
Pasar de datos ficticios en memoria a una consulta **HTTP GET real** a un servicio OData público de demostración. Aprender a procesar JSON con C# y a comparar los conceptos con las **Data Entities** expuestas por Microsoft Dynamics 365 Finance. El servicio utilizado para practicar **no es Dynamics 365 ni contiene información del usuario**.

## Paso 1 — Primera llamada HTTP sin código
Abrir en navegador:
https://services.odata.org/V4/TripPinServiceRW/People?$top=3

Si el servidor público está disponible, debería devolver una representación de una colección `People` con un elemento `value` que contiene registros. A veces el navegador presenta el JSON en texto plano. Guardar solo una captura del contenido público, no de sesiones privadas.

- **Service root**: `https://services.odata.org/V4/TripPinServiceRW/`
- **Entity set**: `People`
- **Query option**: `$top=3` limita los registros devueltos
- **HTTP method**: `GET`
- **Response format**: formato OData/JSON en este servicio de demostración

Luego, experimentar con:
https://services.odata.org/V4/TripPinServiceRW/People?$top=3&$select=UserName,FirstName,LastName

`$select` solicita campos concretos, de forma análoga a elegir columnas en SQL.

Si la API pública está caída, registrar el error (incluyendo HTTP status si es visible) y seguir con la documentación. No declarar éxito sin haber recibido datos.

## Paso 2 — C# (próxima práctica)
Crear una aplicación de consola `.NET 8` llamada `ODataClientLab` en Visual Studio y practicar:
- `HttpClient` y petición GET asíncrona con `await`
- `HttpResponseMessage` y códigos `200 OK`/errores
- `JsonDocument` para recuperar el array `value`
- usar `$top` y `$select` desde el cliente
- control de excepciones de red y pruebas básicas

No se debe inventar una ejecución real de código hasta ver la evidencia del alumno.

## ¿Cómo se conecta esto con F&O?
En Finance, las **Data Entities públicas** se exponen en `https://<URL-de-tu-entorno>/data/<PublicCollectionName>` y publican metadatos en `/data/$metadata`; solamente las entidades habilitadas como públicas aparecen allí. No tenemos todavía credenciales ni un entorno F&O cloud.

En F&O los endpoints requieren autorización mediante Microsoft Entra / OAuth 2.0 y permisos sobre el sistema. Para operaciones entre entidades legales, de forma predeterminada se devuelven datos de la empresa de contexto; con permisos, se puede emplear `cross-company=true` y filtrar por `dataAreaId`, según la entidad y sus capacidades. No confundir permisos de acceso con un filtro cliente voluntario; no usar una URL pública de prueba para inferir seguridad real.

Ejemplo documental de sintaxis F&O, **no ejecutable sin entorno y token autorizado**:

```http
GET https://<URL-del-entorno>/data/CustomersV3?$filter=dataAreaId eq 'usmf'&cross-company=true
Authorization: Bearer <token autorizado>
Accept: application/json
```

`CustomersV3` es un ejemplo documentado por Microsoft; verificar colecciones y campos reales en `/data` y `$metadata` antes de integrar.

## Español / English para entrevistas
- **Application Programming Interface (API)**: interfaz de programación
- **OData / Open Data Protocol**: protocolo de consulta e integración de datos
- **Data Entity**: entidad de datos
- **HTTP GET request**: solicitud de lectura
- **Endpoint**: dirección de un servicio
- **Response / Status Code**: respuesta / código de estado
- **JSON payload**: contenido JSON
- **Authentication (OAuth 2.0)**: autenticación
- **Legal entity / dataAreaId**: sociedad / identificador técnico de sociedad
- **Query options ($filter, $select, $top)**: opciones de filtrado y selección

> I can consume OData endpoints using C# HttpClient, parse JSON responses, and apply query filters. In Dynamics 365 Finance, I understand that public data entities are exposed through the /data endpoint and secured with OAuth 2.0.

Usar la frase completa después de completar el ejercicio de HttpClient; hasta entonces describirlo como objetivo de aprendizaje.

## Fuentes verificadas
- Microsoft Learn — Finance OData: https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/odata
- Microsoft Learn — Service endpoints and authentication: https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/services-home-page
- OData.org — Service demos: https://www.odata.org/odata-services/
- OData.org — Basic tutorial: https://www.odata.org/getting-started/basic-tutorial/
