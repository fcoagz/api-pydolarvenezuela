# pyDolarVenezuela API

La API de pyDolarVenezuela es una herramienta eficiente y confiable que brinda información en tiempo real sobre el valor del dólar y/o euro en Venezuela. Además, facilita la conversión precisa entre bolívares y estas monedas extranjeras.

## URL base

```
https://pydolarvenezuela-api.vercel.app/
``` 

## Endpoints

### `GET /`

Este endpoint muestra un mensaje de bienvenida y proporciona un enlace a la documentación de la API.

### `GET /api/v1/<currency>`

Este endpoint permite obtener todas las entidades de seguimiento del dólar y/o euro, junto con su nombre correspondiente, cambio y fecha de la última actualización. Ademas permite obtener información sobre el monitor en una página específica. Las páginas disponibles son: `bcv`, `criptodolar`, `exchangemonitor`.

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | _Opcional._ Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | _Opcional._ Indica el monitor específico. |


### `GET /api/v1/<currency>/conversion`

Este endpoint convierte un valor en bolívares a su equivalente a estas monedas extranjeras y viceversa.

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| type       | `string` | Indica el tipo de conversión. Puede ser `VES` o `USD` o `EUR`. |
| value      | `float or integer` | Indica el valor a convertir. |
| monitor    | `string` | Indica el monitor específico. |

## Uso
Para obtener información actualizada sobre el precio del dólar en Venezuela de `EnParaleloVzla`, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/unit/enparalelovzla"
```

Para obtener información sobre el dólar en una página específica, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
```

## Variables de entorno
pyDolarVenezuela utiliza Redis Cloud, un motor de base de datos en memoria, para almacenar y procesar datos. 

- `RADIS_HOST`
- `RADIS_PORT`
- `RADIS_PASSWORD`