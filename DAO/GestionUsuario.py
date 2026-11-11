
import bcrypt
from DAO.Conexion import conectar


def registrar_usuario(
    username,
    password,
    nombre,
    apellido,
    email,
    empleado_id
):
    """
    Registra una cuenta de empleado vinculada a un empleado existente.
    No permite crear cuentas de administrador desde este procedimiento.
    """

    conexion = conectar()

    if conexion is None:
        return False

    cursor = None

    try:
        username = username.strip()
        nombre = nombre.strip()
        apellido = apellido.strip()
        email = email.strip()

        if not all([username, password, nombre, apellido, email]):
            print("Error: todos los campos son obligatorios.")
            return False

        if empleado_id is None:
            print("Error: debes seleccionar un empleado existente.")
            return False

        cursor = conexion.cursor()

        cursor.execute(
            "SELECT user_id FROM empleado WHERE user_id = %s",
            (empleado_id,)
        )

        if cursor.fetchone() is None:
            print("Error: el empleado seleccionado no existe.")
            return False

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        sql = """
            INSERT INTO usuarios (
                username,
                password_hash,
                nombre,
                apellido,
                email,
                tipo,
                empleado_id
            )
            VALUES (%s, %s, %s, %s, %s, 'empleado', %s)
        """

        cursor.execute(
            sql,
            (
                username,
                password_hash,
                nombre,
                apellido,
                email,
                empleado_id
            )
        )

        conexion.commit()
        print("Cuenta de empleado registrada correctamente.")
        return True

    except Exception as error:
        print("Error: no se pudo registrar el usuario.")

        try:
            conexion.rollback()
        except Exception:
            pass

        return False

    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass

        try:
            conexion.close()
        except Exception:
            pass


def usuario_existe(username):
    conexion = conectar()

    if conexion is None:
        return None

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT id
            FROM usuarios
            WHERE username = %s
        """

        cursor.execute(sql, (username,))
        return cursor.fetchone() is not None

    except Exception:
        print("Error: no se pudo verificar el usuario.")
        return None

    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass

        try:
            conexion.close()
        except Exception:
            pass


def iniciar_sesion(username, password):
    conexion = conectar()

    if conexion is None:
        return None

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT
                id,
                username,
                password_hash,
                nombre,
                apellido,
                email,
                tipo,
                empleado_id
            FROM usuarios
            WHERE username = %s
        """

        cursor.execute(sql, (username,))
        usuario = cursor.fetchone()

        if usuario is None:
            return None

        password_hash = usuario[2].encode("utf-8")

        if bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash
        ):
            return {
                "id": usuario[0],
                "username": usuario[1],
                "nombre": usuario[3],
                "apellido": usuario[4],
                "email": usuario[5],
                "tipo": usuario[6],
                "empleado_id": usuario[7]
            }

        return None

    except Exception:
        print("Error: no se pudo completar el inicio de sesión.")
        return None

    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass

        try:
            conexion.close()
        except Exception:
            pass


def listar_empleados_sin_cuenta():
    """
    Devuelve los empleados que todavía no tienen una cuenta asociada.
    """

    conexion = conectar()

    if conexion is None:
        return None

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT
                e.user_id,
                e.nombre,
                e.correo
            FROM empleado e
            LEFT JOIN usuarios u
                ON u.empleado_id = e.user_id
            WHERE u.id IS NULL
            ORDER BY e.nombre
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception:
        print("Error: no se pudieron consultar los empleados disponibles.")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()


def listar_cuentas_usuario():
    """
    Devuelve las cuentas registradas sin mostrar sus contraseñas.
    """

    conexion = conectar()

    if conexion is None:
        return None

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
            SELECT
                id,
                username,
                nombre,
                apellido,
                email,
                tipo,
                empleado_id
            FROM usuarios
            ORDER BY id
        """

        cursor.execute(sql)
        return cursor.fetchall()

    except Exception:
        print("Error: no se pudieron consultar las cuentas.")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()



def registrar_administrador(
    username,
    password,
    nombre,
    apellido,
    email
):
    """
    Registra una cuenta administrativa sin vincularla
    a un empleado.
    """

    conexion = conectar()

    if conexion is None:
        return False

    cursor = None

    try:
        username = username.strip()
        nombre = nombre.strip()
        apellido = apellido.strip()
        email = email.strip()

        if not all([username, password, nombre, apellido, email]):
            print("Error: todos los campos son obligatorios.")
            return False

        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id FROM usuarios WHERE username = %s",
            (username,)
        )

        if cursor.fetchone() is not None:
            print("Error: ese nombre de usuario ya está registrado.")
            return False

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        sql = """
            INSERT INTO usuarios (
                username,
                password_hash,
                nombre,
                apellido,
                email,
                tipo,
                empleado_id
            )
            VALUES (%s, %s, %s, %s, %s, 'administrador', NULL)
        """

        cursor.execute(
            sql,
            (
                username,
                password_hash,
                nombre,
                apellido,
                email
            )
        )

        conexion.commit()
        print("Cuenta de administrador registrada correctamente.")
        return True

    except Exception:
        print("Error: no se pudo registrar la cuenta administrativa.")

        try:
            conexion.rollback()
        except Exception:
            pass

        return False

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()
