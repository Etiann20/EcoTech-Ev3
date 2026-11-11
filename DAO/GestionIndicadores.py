
import requests


URL_API = "https://indicadores.cl/api/v1/hoy.json"


def obtener_indicador(nombre_indicador):

    indicadores_permitidos = {
        "dolar": "Dólar observado",
        "euro": "Euro",
        "uf": "Unidad de Fomento",
        "utm": "Unidad Tributaria Mensual"
    }

    if not isinstance(nombre_indicador, str):
        print("Error: debes ingresar un indicador válido.")
        return None

    nombre_indicador = nombre_indicador.strip().lower()

    if nombre_indicador not in indicadores_permitidos:
        print("Indicador no válido.")
        return None

    try:
        respuesta = requests.get(URL_API, timeout=10)
        respuesta.raise_for_status()

        datos = respuesta.json()

        if not isinstance(datos, dict):
            print("Error: la API entregó una respuesta inválida.")
            return None

        indicador = datos.get(nombre_indicador)

        if not isinstance(indicador, dict):
            print("La API no entregó el indicador solicitado.")
            return None

        valor = indicador.get("valor")

        if nombre_indicador == "utm":
            fecha = indicador.get("mes")
        else:
            fecha = indicador.get("fecha")

        if type(valor) not in (int, float):
            print("Error: el valor recibido no es válido.")
            return None

        if not isinstance(fecha, str) or not fecha.strip():
            print("Error: la fecha del indicador no es válida.")
            return None

        return {
            "nombre": indicadores_permitidos[nombre_indicador],
            "valor": valor,
            "fecha": fecha
        }

    except requests.exceptions.Timeout:
        print("Error: la consulta a indicadores.cl superó el tiempo de espera.")

    except requests.exceptions.HTTPError as error:
        codigo_http = (
            error.response.status_code
            if error.response is not None
            else 0
        )

        if codigo_http == 404:
            print("Error HTTP 404: el recurso solicitado no fue encontrado.")
        elif codigo_http == 500:
            print("Error HTTP 500: el servidor de indicadores.cl presenta problemas.")
        elif codigo_http in (502, 503, 504):
            print(f"Error HTTP {codigo_http}: indicadores.cl no está disponible.")
        else:
            print(f"Error HTTP {codigo_http}: no se pudo completar la consulta.")

    except requests.exceptions.ConnectionError:
        print("Error: no fue posible establecer conexión con indicadores.cl.")

    except requests.exceptions.RequestException:
        print("Error: ocurrió un problema durante la consulta a indicadores.cl.")

    except (ValueError, TypeError, KeyError):
        print("Error: la respuesta de indicadores.cl tiene un formato inválido.")

    except Exception:
        print("Error: ocurrió un problema inesperado durante la consulta.")

    return None


def mostrar_indicador(nombre_indicador):
    resultado = obtener_indicador(nombre_indicador)

    if resultado is None:
        return

    print("\n--- INDICADOR ECONÓMICO ---")
    print("Indicador:", resultado["nombre"])
    print("Valor:", resultado["valor"])

    if nombre_indicador.strip().lower() == "utm":
        print("Mes:", resultado["fecha"])
    else:
        print("Fecha:", resultado["fecha"])

    print("Fuente: https://indicadores.cl/api/")
