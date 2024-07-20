# pyDolarVenezuela API

La API de pyDolarVenezuela es una herramienta eficiente y confiable que brinda información en tiempo real sobre el valor del dólar y/o euro en Venezuela. Además, facilita la conversión precisa entre bolívares y estas monedas extranjeras.

Swagger API: https://pydolarvenezuela-api.vercel.app/apidocs

## URL base

```
https://pydolarvenezuela-api.vercel.app/
``` 

## Endpoints

### `GET /`

Este endpoint muestra un mensaje de bienvenida y proporciona un enlace a la documentación de la API.

### `GET /api/v1/<currency>`

Este endpoint permite obtener todas las entidades de seguimiento del dólar y/o euro, junto con su nombre correspondiente, cambio y fecha de la última actualización. Ademas permite obtener información sobre el monitor en una página específica. Las páginas disponibles son: `alcambio`, `bcv`, `criptodolar`, `dolartoday`, `exchangemonitor`, `enparalelovzla`, `italcambio`.

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

## Actividad

![Alt](https://repobeats.axiom.co/api/embed/7fc602e88410dfba302fe708f14e0e30d059a729.svg "Repobeats analytics image")

## Uso
Para obtener información actualizada sobre el precio del dólar en Venezuela de `EnParaleloVzla`, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/unit/enparalelovzla"
```

Para obtener información sobre el dólar en una página específica, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
```

## Sponsors

<a href="https://www.capasiete.com/" target="_blank" title="Capa7, proveedor de servicios web hosting, streaming y servidores, servicios rápidos, confiables, y seguros, 99.9% óptimo, soporte 24/7."><img src="https://github.com/fcoagz/api-pydolarvenezuela/blob/main/assets/capasiete.jpg?raw=true" width="250" height="150"></a>
<a href="https://criptomerkado.com/" target="_blank" title="Somos una plataforma para compra y venta de cripto monedas." ><img src="https://github.com/fcoagz/api-pydolarvenezuela/blob/main/assets/criptomerkado.jpg?raw=true
" width="250" height="150"></a>

## Variables de entorno
pyDolarVenezuela utiliza SQLAlchemy para la integración de la base de datos Postgres. [Más información](https://github.com/fcoagz/pydolarvenezuela?tab=readme-ov-file#base-de-datos)

- `SQL_MOTOR`
- `SQL_HOST`
- `SQL_DB_NAME`
- `SQL_PORT`
- `SQL_USER`
- `SQL_PASSWORD`

## Contributores

<a href="https://github.com/fcoagz/api-pydolarvenezuela/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fcoagz/api-pydolarvenezuela"/>
</a>