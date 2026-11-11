from DAO.Conexion import conectar


def validar_asignacion(cursor, empleado_id, proyecto_id):
    """Comprueba empleado, proyecto y asignación entre ambos."""

    cursor.execute(
        "SELECT user_id FROM empleado WHERE user_id = %s",
        (empleado_id,)
    )
    if not cursor.fetchone():
        print("Error: el empleado seleccionado no existe.")
        return False

    cursor.execute(
        "SELECT user_id FROM proyecto WHERE user_id = %s",
        (proyecto_id,)
    )
    if not cursor.fetchone():
        print("Error: el proyecto seleccionado no existe.")
        return False

    cursor.execute(
        """
        SELECT asignacion_id
        FROM asignacion_emp
        WHERE empleado_id = %s AND proyecto_id = %s
        """,
        (empleado_id, proyecto_id)
    )

    if not cursor.fetchone():
        print("Error: el empleado no está asignado a este proyecto.")
        return False

    return True


def validar_horas(horas):
    try:
        if int(horas) <= 0:
            print("Error: las horas trabajadas deben ser mayores que cero.")
            return False
    except (TypeError, ValueError):
        print("Error: las horas deben ser un número entero válido.")
        return False

    return True


def insertar(registro):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        if not validar_horas(registro.horas):
            return False

        if not validar_asignacion(
            cursor,
            registro.empleado_id,
            registro.proyecto_id
        ):
            return False

        cursor.execute(
            """
            INSERT INTO registro_tiempo
                (empleado_id, proyecto_id, fecha, horas, descripcion)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                registro.empleado_id,
                registro.proyecto_id,
                registro.fecha,
                registro.horas,
                registro.descripcion
            )
        )

        registro.user_id = cursor.lastrowid
        conexion.commit()

        print(
            "Registro de tiempo creado correctamente. "
            f"ID: {registro.user_id}"
        )
        return True

    except Exception:
        conexion.rollback()
        print("Error: no fue posible registrar el tiempo.")
        return False

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def consultar():
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return []

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT
                rt.user_id,
                rt.empleado_id,
                e.nombre,
                rt.proyecto_id,
                p.nombre,
                rt.fecha,
                rt.horas,
                rt.descripcion
            FROM registro_tiempo AS rt
            LEFT JOIN empleado AS e
                ON rt.empleado_id = e.user_id
            LEFT JOIN proyecto AS p
                ON rt.proyecto_id = p.user_id
            ORDER BY rt.user_id
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception:
        print("Error: no fue posible consultar los registros de tiempo.")
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def modificar(registro):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT user_id FROM registro_tiempo WHERE user_id = %s",
            (registro.user_id,)
        )

        if not cursor.fetchone():
            print("Error: el registro de tiempo no existe.")
            return False

        if not validar_horas(registro.horas):
            return False

        if not validar_asignacion(
            cursor,
            registro.empleado_id,
            registro.proyecto_id
        ):
            return False

        cursor.execute(
            """
            UPDATE registro_tiempo
            SET empleado_id = %s,
                proyecto_id = %s,
                fecha = %s,
                horas = %s,
                descripcion = %s
            WHERE user_id = %s
            """,
            (
                registro.empleado_id,
                registro.proyecto_id,
                registro.fecha,
                registro.horas,
                registro.descripcion,
                registro.user_id
            )
        )

        if cursor.rowcount > 0:
            conexion.commit()
            print("Registro de tiempo modificado correctamente.")
            return True

        conexion.rollback()
        print("No se detectaron cambios en el registro.")
        return False

    except Exception:
        conexion.rollback()
        print("Error: no fue posible modificar el registro de tiempo.")
        return False

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM registro_tiempo WHERE user_id = %s",
            (user_id,)
        )

        if cursor.rowcount > 0:
            conexion.commit()
            print("Registro de tiempo eliminado correctamente.")
            return True

        conexion.rollback()
        print("No existe un registro de tiempo con ese ID.")
        return False

    except Exception:
        conexion.rollback()
        print("Error: no fue posible eliminar el registro de tiempo.")
        return False

    finally:
        if cursor:
            cursor.close()
        conexion.close()
