
from DAO.Conexion import conectar


def insertar(departamento):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        if departamento.gerente_empleado_id is not None:
            cursor.execute(
                "SELECT user_id FROM empleado WHERE user_id = %s",
                (departamento.gerente_empleado_id,)
            )

            if not cursor.fetchone():
                print("Error: el gerente seleccionado no existe.")
                return

        cursor.execute(
            """
            INSERT INTO departamento
                (nombre, gerente_empleado_id, descripcion)
            VALUES (%s, %s, %s)
            """,
            (
                departamento.nombre,
                departamento.gerente_empleado_id,
                departamento.descripcion
            )
        )

        departamento.user_id = cursor.lastrowid
        conexion.commit()

        print(
            "Departamento registrado correctamente. "
            f"ID: {departamento.user_id}"
        )

    except Exception:
        conexion.rollback()
        print("Error: no fue posible registrar el departamento.")

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

        cursor.execute(
            """
            SELECT
                user_id,
                nombre,
                gerente_empleado_id,
                descripcion
            FROM departamento
            ORDER BY user_id
            """
        )

        return cursor.fetchall()

    except Exception:
        print("Error: no fue posible consultar los departamentos.")
        return []

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def modificar(departamento):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT user_id FROM departamento WHERE user_id = %s",
            (departamento.user_id,)
        )

        if not cursor.fetchone():
            print("Error: el departamento seleccionado no existe.")
            return

        if departamento.gerente_empleado_id is not None:
            cursor.execute(
                "SELECT user_id FROM empleado WHERE user_id = %s",
                (departamento.gerente_empleado_id,)
            )

            if not cursor.fetchone():
                print("Error: el gerente seleccionado no existe.")
                return

        cursor.execute(
            """
            UPDATE departamento
            SET nombre = %s,
                gerente_empleado_id = %s,
                descripcion = %s
            WHERE user_id = %s
            """,
            (
                departamento.nombre,
                departamento.gerente_empleado_id,
                departamento.descripcion,
                departamento.user_id
            )
        )

        if cursor.rowcount > 0:
            conexion.commit()
            print("Departamento modificado correctamente.")
        else:
            conexion.rollback()
            print("No se detectaron cambios en el departamento.")

    except Exception:
        conexion.rollback()
        print("Error: no fue posible modificar el departamento.")

    finally:
        if cursor:
            cursor.close()
        conexion.close()


def eliminar(user_id):
    conexion = conectar()

    if not conexion:
        print("No fue posible conectar con la base de datos.")
        return

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT user_id FROM departamento WHERE user_id = %s",
            (user_id,)
        )

        if not cursor.fetchone():
            print("No existe un departamento con ese ID.")
            return

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM empleado
            WHERE departamento_id = %s
            """,
            (user_id,)
        )

        if cursor.fetchone()[0] > 0:
            print(
                "\nNo se puede eliminar el departamento porque "
                "tiene empleados asociados."
            )
            print("Reasigna primero esos empleados a otro departamento.")
            return

        cursor.execute(
            "DELETE FROM departamento WHERE user_id = %s",
            (user_id,)
        )

        if cursor.rowcount > 0:
            conexion.commit()
            print("Departamento eliminado correctamente.")
        else:
            conexion.rollback()
            print("No se pudo eliminar el departamento.")

    except Exception:
        conexion.rollback()
        print("Error: no fue posible eliminar el departamento.")

    finally:
        if cursor:
            cursor.close()
        conexion.close()
