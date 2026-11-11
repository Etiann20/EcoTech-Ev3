
class RegistroTiempo:

    def __init__(
        self,
        empleado_id,
        proyecto_id,
        fecha,
        horas,
        descripcion,
        user_id=None
    ):
        self.__user_id = user_id
        self.__empleado_id = empleado_id
        self.__proyecto_id = proyecto_id
        self.__fecha = fecha
        self.__horas = horas
        self.__descripcion = descripcion

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valor):
        self.__user_id = valor

    @property
    def empleado_id(self):
        return self.__empleado_id

    @empleado_id.setter
    def empleado_id(self, valor):
        self.__empleado_id = valor

    @property
    def proyecto_id(self):
        return self.__proyecto_id

    @proyecto_id.setter
    def proyecto_id(self, valor):
        self.__proyecto_id = valor

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, valor):
        self.__fecha = valor

    @property
    def horas(self):
        return self.__horas

    @horas.setter
    def horas(self, valor):
        self.__horas = valor

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self.__descripcion = valor

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"Empleado: {self.empleado_id} | "
            f"Proyecto: {self.proyecto_id} | "
            f"Fecha: {self.fecha} | "
            f"Horas: {self.horas} | "
            f"Descripción: {self.descripcion}"
        )
