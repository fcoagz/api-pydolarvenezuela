# pyDolarVenezuela API

La API de pyDolarVenezuela es una herramienta eficiente y confiable que brinda información en tiempo real sobre el valor del dólar y euro en Venezuela. Además, facilita la conversión precisa entre bolívares y estas monedas extranjeras.

Swagger API: http://pydolarve.org/apidocs

## URL base

```
http://pydolarve.org/
```

## Endpoints

### `GET /`

Este endpoint muestra un mensaje de bienvenida y proporciona un enlace a la documentación de la API.

### `GET /api/v1/<currency>`

Este endpoint permite obtener todas las entidades de seguimiento del dólar y/o euro, junto con su nombre correspondiente, cambio y fecha de la última actualización. Ademas permite obtener información sobre el monitor en una página específica. Las páginas disponibles son: `alcambio`, `bcv`, `criptodolar`, `dolartoday`, `enparalelovzla`, `italcambio`.

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | _Opcional._ Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | _Opcional._ Indica el monitor específico. |

### `GET /api/v1/<currency>/history`

Este endpoint le permite conocer el historial de precios de un monitor especificando la fecha de inicio y finalización.

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

Header:
- `Authorization`: El token de autorización correspondiente al usuario.

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | Indica el monitor específico. |
| start_date    | `string` | Fecha de inicio del historial. `DD-MM-YYYY` |
| end_date   | `string` | Fecha de fin del historial. `DD-MM-YYYY` |

### `GET /api/v1/<currency>/changes`

Este endpoint permite conocer los cambios que ha obtenido el monitor en un día concreto. (Actualizaciones de precios)

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

Header:
- `Authorization`: El token de autorización correspondiente al usuario.

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | Indica el monitor específico. |
| date    | `string` | Fecha de la cual se desea obtener los precios. `DD-MM-YYYY` |

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
curl -X GET "http://pydolarve.org/api/v1/dollar?monitor=enparalelovzla"
```

Para obtener información sobre el dólar en una página específica, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "http://pydolarve.org/api/v1/dollar?page=bcv"
```

## Sponsors

<a href="https://www.capasiete.com/" target="_blank" title="Capa7, proveedor de servicios web hosting, streaming y servidores, servicios rápidos, confiables, y seguros, 99.9% óptimo, soporte 24/7."><img src="https://github.com/fcoagz/api-pydolarvenezuela/blob/main/assets/sponsor/capasiete.jpg?raw=true" width="250" height="150"></a>
<a href="https://criptomerkado.com/" target="_blank" title="Somos una plataforma para compra y venta de cripto monedas." ><img src="https://github.com/fcoagz/api-pydolarvenezuela/blob/main/assets/sponsor/criptomerkado.jpg?raw=true" width="250" height="150"></a>

## Apoya este proyecto

Si deseas conocer características interesantes de la API de por vida, considera hacer una donación o suscribirte a través de [Ko-fi](https://ko-fi.com/fcoagz). Tu apoyo contribuirá al continuo desarrollo del proyecto y al mantenimiento de los servicios en los que está alojado.

| Características | Gratis | Token |
| --------------- | ------ | ------ |
| Solicitudes API | 100/hora | ∞ |
| Historial de precios | No | Sí |
| Obtención de fuentes directas en un solo lugar | Por separado | Sí |

Envíame un mensaje privado desde Ko-fi para que pueda proporcionarte el token de acceso.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O5O5RFF4T)

## Contributores

<a href="https://github.com/fcoagz/api-pydolarvenezuela/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fcoagz/api-pydolarvenezuela"/>
</a>