import requests


URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
URL_CLIMA = "https://api.open-meteo.com/v1/forecast"


def obtener_clima(ciudad):

    if not isinstance(ciudad, str):
        print("Error: debes ingresar un nombre de ciudad válido.")
        return None

    ciudad = ciudad.strip()

    if len(ciudad) < 2 or len(ciudad) > 100:
        print(
            "Error: ingresa un nombre de ciudad válido "
            "(entre 2 y 100 caracteres)."
        )
        return None

    try:
        respuesta_ciudad = requests.get(
            URL_GEOCODING,
            params={
                "name": ciudad,
                "count": 1,
                "language": "es",
                "format": "json"
            },
            timeout=10
        )

        respuesta_ciudad.raise_for_status()
        datos_ciudad = respuesta_ciudad.json()

        resultados = datos_ciudad.get("results")

        if not isinstance(resultados, list) or not resultados:
            print("No se encontró la ciudad ingresada.")
            return None

        ubicacion = resultados[0]

        latitud = ubicacion["latitude"]
        longitud = ubicacion["longitude"]
        nombre = ubicacion["name"]
        pais = ubicacion.get("country", "No identificado")

        respuesta_clima = requests.get(
            URL_CLIMA,
            params={
                "latitude": latitud,
                "longitude": longitud,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "weather_code"
                ),
                "timezone": "auto"
            },
            timeout=10
        )

        respuesta_clima.raise_for_status()
        datos_clima = respuesta_clima.json()

        actual = datos_clima.get("current")

        if not isinstance(actual, dict):
            print("La API no entregó datos climáticos válidos.")
            return None

        codigo = actual.get("weather_code")

        condiciones = {
            0: "Despejado",
            1: "Mayormente despejado",
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Niebla",
            48: "Niebla con escarcha",
            51: "Llovizna ligera",
            53: "Llovizna moderada",
            55: "Llovizna intensa",
            61: "Lluvia ligera",
            63: "Lluvia moderada",
            65: "Lluvia intensa",
            71: "Nevada ligera",
            73: "Nevada moderada",
            75: "Nevada intensa",
            80: "Chubascos ligeros",
            81: "Chubascos moderados",
            82: "Chubascos intensos",
            95: "Tormenta eléctrica"
        }

        return {
            "ciudad": nombre,
            "pais": pais,
            "temperatura": actual.get("temperature_2m"),
            "humedad": actual.get("relative_humidity_2m"),
            "condicion": condiciones.get(
                codigo,
                "Condición no identificada"
            ),
            "fecha": actual.get("time")
        }

    except requests.exceptions.Timeout:
        print("Error: la consulta climática excedió el tiempo límite.")

    except requests.exceptions.HTTPError as error:
        codigo_http = error.response.status_code if error.response is not None else 0

        if codigo_http == 404:
            print("Error HTTP 404: el recurso solicitado no fue encontrado.")
        elif codigo_http == 500:
            print("Error HTTP 500: el servidor climático presenta problemas.")
        elif codigo_http in (502, 503, 504):
            print(f"Error HTTP {codigo_http}: el servicio climático no está disponible.")
        else:
            print(f"Error HTTP {codigo_http}: no se pudo completar la consulta.")

    except requests.exceptions.ConnectionError:
        print("Error: no fue posible establecer conexión con el servicio climático.")

    except requests.exceptions.RequestException:
        print("Error: ocurrió un problema durante la consulta climática.")

    except (ValueError, TypeError, KeyError):
        print("Error: la respuesta de la API tiene un formato inválido.")

    except Exception:
        print("Error: ocurrió un problema inesperado durante la consulta.")

    return None


def mostrar_clima(ciudad):
    datos = obtener_clima(ciudad)

    if datos is None:
        return False

    print("\n========== INFORMACIÓN CLIMÁTICA ==========")
    print(f"Ciudad: {datos['ciudad']}, {datos['pais']}")
    print(f"Temperatura: {datos['temperatura']} °C")
    print(f"Humedad: {datos['humedad']} %")
    print(f"Estado del tiempo: {datos['condicion']}")
    print(f"Fecha y hora: {datos['fecha']}")

    return True
