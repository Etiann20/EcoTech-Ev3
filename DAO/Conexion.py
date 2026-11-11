import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def conectar():
    try:
        conexion = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )

        return conexion

    except Exception:
        print(
            "Error: No se pudo acceder a la base de datos. "
            "Verifica la configuración de conexión."
        )
        return None
