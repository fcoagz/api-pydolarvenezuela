# pyDolarVenezuela API
La API de pyDolarVenezuela permite obtener información actualizada sobre el precio del dólar en Venezuela, así como realizar conversiones de bolívares a dólares y viceversa.
## URL base
```
https://pydolarvenezuela-api.vercel.app/
``` 
## Endpoints
`GET /`: Muestra un mensaje de bienvenida y proporciona un enlace a la documentación de la API.

`GET /api/v1/dollar/`: Permite obtener todas las entidades de seguimiento del dólar con su respectivo nombre, cambio y fecha de última actualización.

`GET /api/v1/dollar/{section_dollar}`: Obtiene información sobre el precio del dólar en Venezuela en una sección específica.

Parámetros:

- `section_dollar` (requerido): una cadena que indica la sección deseada. Las secciones disponibles son: `dolar_promedio`, `bcv_oficial`, `paginas`, `monederos_electronicos`.

`GET /api/v1/dollar/{section_dollar}/{key_monitor}`: Obtiene información sobre el precio del dólar en Venezuela en una sección y un monitor específicos.

Parámetros:

- `section_dollar` (requerido): una cadena que indica la sección deseada. Las secciones disponibles son: `dolar_promedio`, `bcv_oficial`, `paginas`, `monederos_electronicos`.

- `key_monitor` (requerido): una cadena que indica el monitor específico. Las claves de los monitores disponibles varían según la sección.

`GET /api/v1/dollar/td/{value}/{key_monitor}`: Convierte un valor en bolívares a su equivalente en dólares estadounidenses.

`GET /api/v1/dollar/tb/{value}/{key_monitor}`: Convierte un valor en dólares estadounidenses a su equivalente en bolívares.

Parámetros:

- `value` (requerido): una cadena que indica el valor en bolívares a convertir.
- `key_monitor` (requerido): una cadena que indica el monitor específico.

## Uso
Para obtener información sobre el precio del dólar en Venezuela en la sección `dolar_promedio`, se puede hacer una solicitud GET a la siguiente URL:

```
https://pydolarvenezuela-api.vercel.app/api/v1/dollar/dolar_promedio
```

La respuesta es objeto JSON que contiene la información solicitada.