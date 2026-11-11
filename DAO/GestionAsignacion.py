from DAO.Conexion import conectar


def insertar(asignacion):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT user_id FROM empleado WHERE user_id = %s",
            (asignacion.empleado_id,)
        )
        if not cursor.fetchone():
            print("Error: el empleado seleccionado no existe.")
            return

        cursor.execute(
            "SELECT user_id FROM proyecto WHERE user_id = %s",
            (asignacion.proyecto_id,)
        )
        if not cursor.fetchone():
            print("Error: el proyecto seleccionado no existe.")
            return

        cursor.execute(
            """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE empleado_id = %s AND proyecto_id = %s
            """,
            (asignacion.empleado_id, asignacion.proyecto_id)
        )

        if cursor.fetchone():
            print("Error: el empleado ya está asignado a ese proyecto.")
            return

        cursor.execute(
            """
            INSERT INTO asignacion_emp
                (empleado_id, proyecto_id, rol)
            VALUES (%s, %s, %s)
            """,
            (
                asignacion.empleado_id,
                asignacion.proyecto_id,
                asignacion.rol
            )
        )

        asignacion.asignacion_id = cursor.lastrowid
        conexion.commit()

        print(
            "Asignación registrada correctamente. "
            f"ID: {asignacion.asignacion_id}"
        )

    except Exception:
        conexion.rollback()
        print("Error: no fue posible registrar la asignación.")

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
                a.asignacion_id,
                a.empleado_id,
                e.nombre,
                a.proyecto_id,
                p.nombre,
                a.rol
            FROM asignacion_emp AS a
            LEFT JOIN empleado AS e
                ON a.empleado_id = e.user_id
            LEFT JOIN proyecto AS p
                ON a.proyecto_id = p.user_id
            ORDER BY a.asignacion_id
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception:
        print("Error: no fue posible consultar las asignaciones.")
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def modificar(asignacion):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE asignacion_id = %s
            """,
            (asignacion.asignacion_id,)
        )

        if not cursor.fetchone():
            print("Error: la asignación no existe.")
            return

        cursor.execute(
            "SELECT user_id FROM empleado WHERE user_id = %s",
            (asignacion.empleado_id,)
        )
        if not cursor.fetchone():
            print("Error: el empleado seleccionado no existe.")
            return

        cursor.execute(
            "SELECT user_id FROM proyecto WHERE user_id = %s",
            (asignacion.proyecto_id,)
        )
        if not cursor.fetchone():
            print("Error: el proyecto seleccionado no existe.")
            return

        cursor.execute(
            """
            SELECT asignacion_id
            FROM asignacion_emp
            WHERE empleado_id = %s
              AND proyecto_id = %s
              AND asignacion_id != %s
            """,
            (
                asignacion.empleado_id,
                asignacion.proyecto_id,
                asignacion.asignacion_id
            )
        )

        if cursor.fetchone():
            print("Error: el empleado ya está asignado a ese proyecto.")
            return

        cursor.execute(
            """
            SELECT empleado_id, proyecto_id
            FROM asignacion_emp
            WHERE asignacion_id = %s
            """,
            (asignacion.asignacion_id,)
        )
        actual = cursor.fetchone()

        if actual and (
            actual[0] != asignacion.empleado_id
            or actual[1] != asignacion.proyecto_id
        ):
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM registro_tiempo
                WHERE empleado_id = %s AND proyecto_id = %s
                """,
                (actual[0], actual[1])
            )

            if cursor.fetchone()[0] > 0:
                print(
                    "No se puede cambiar el empleado o proyecto de "
                    "esta asignación porque existen registros de tiempo."
                )
                return

        cursor.execute(
            """
            UPDATE asignacion_emp
            SET empleado_id = %s,
                proyecto_id = %s,
                rol = %s
            WHERE asignacion_id = %s
            """,
            (
                asignacion.empleado_id,
                asignacion.proyecto_id,
                asignacion.rol,
                asignacion.asignacion_id
            )
        )

        if cursor.rowcount > 0:
            conexion.commit()
            print("Asignación modificada correctamente.")
        else:
            conexion.rollback()
            print("No se detectaron cambios en la asignación.")

    except Exception:
        conexion.rollback()
        print("Error: no fue posible modificar la asignación.")

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def eliminar(asignacion_id):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT empleado_id, proyecto_id
            FROM asignacion_emp
            WHERE asignacion_id = %s
            """,
            (asignacion_id,)
        )
        asignacion = cursor.fetchone()

        if not asignacion:
            print("No existe una asignación con ese ID.")
            return

        empleado_id, proyecto_id = asignacion

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM registro_tiempo
            WHERE empleado_id = %s AND proyecto_id = %s
            """,
            (empleado_id, proyecto_id)
        )

        if cursor.fetchone()[0] > 0:
            print(
                "\nNo se puede eliminar esta asignación porque "
                "existen registros de tiempo para ese empleado "
                "y proyecto."
            )
            print("Elimina o gestiona primero esos registros.")
            return

        cursor.execute(
            "DELETE FROM asignacion_emp WHERE asignacion_id = %s",
            (asignacion_id,)
        )

        if cursor.rowcount > 0:
            conexion.commit()
            print("Asignación eliminada correctamente.")
        else:
            conexion.rollback()
            print("No se pudo eliminar la asignación.")

    except Exception:
        conexion.rollback()
        print("Error: no fue posible eliminar la asignación.")

    finally:
        if cursor:
            cursor.close()
        conexion.close()



def consultar_proyectos_empleado(empleado_id):
    """
    Consulta los proyectos a los que está asignado
    un empleado específico.
    """

    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return None

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT
                p.user_id,
                p.nombre,
                a.rol
            FROM asignacion_emp AS a
            INNER JOIN proyecto AS p
                ON a.proyecto_id = p.user_id
            WHERE a.empleado_id = %s
            ORDER BY p.nombre
        """

        cursor.execute(sql, (empleado_id,))
        return cursor.fetchall()

    except Exception:
        print("Error: no fue posible consultar los proyectos asignados.")
        return None

    finally:
        if cursor:
            cursor.close()
        conexion.close()
