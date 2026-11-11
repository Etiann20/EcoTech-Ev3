
class Departamento:

    def __init__(
        self,
        nombre,
        descripcion,
        gerente_empleado_id=None,
        user_id=None
    ):
        self.__user_id = user_id
        self.__nombre = nombre
        self.__gerente_empleado_id = gerente_empleado_id
        self.__descripcion = descripcion

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valor):
        self.__user_id = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def gerente_empleado_id(self):
        return self.__gerente_empleado_id

    @gerente_empleado_id.setter
    def gerente_empleado_id(self, valor):
        self.__gerente_empleado_id = valor

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self.__descripcion = valor

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"Nombre: {self.nombre} | "
            f"Gerente: {self.gerente_empleado_id} | "
            f"Descripción: {self.descripcion}"
        )
