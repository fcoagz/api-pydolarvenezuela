# pyDolarVenezuela API

La API de pyDolarVenezuela permite obtener información actualizada sobre el precio del dólar en Venezuela, así como realizar conversiones de bolívares a dólares y viceversa.

## URL base

```
https://pydolarvenezuela-api.vercel.app/
``` 

## Endpoints

### `GET /`

Este endpoint muestra un mensaje de bienvenida y proporciona un enlace a la documentación de la API.

### `GET /api/v1/dollar/`

Este endpoint permite obtener todas las entidades de seguimiento del dólar con su respectivo nombre, cambio y fecha de última actualización.

### `GET /api/v1/dollar/history`

Este endpoint te permite acceder al historial de los precios del dólar. Los datos se actualizan y se restablece semanalmente, este endpoint ofrece la posibilidad de consultar hasta 10 monitores diferentes para obtener una visión más completa del comportamiento del mercado.

### `GET /api/v1/dollar/page`

Este endpoint permite obtener información sobre el dólar en una página específica. Las páginas disponibles son: `bcv`, `criptodolar`, `exchangemonitor`, `ivenezuela`, `dpedidos`.

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | _Opcional._ Indica el monitor específico. |

### `GET /api/v1/dollar/conversion`

Este endpoint convierte un valor en bolívares a su equivalente en dólares estadounidenses y viceversa.

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| type       | `string` | Indica el tipo de conversión. Puede ser `VES` o `USD`. |
| value      | `float or integer` | Indica el valor a convertir. |
| monitor    | `string` | Indica el monitor específico. |

## Uso
Para obtener información actualizada sobre el precio del dólar en Venezuela de `EnParaleloVzla`, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/unit/enparalelovzla"
```

Para obtener información sobre el dólar en una página específica, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/page?page=bcv"
```
