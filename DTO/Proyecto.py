
class Proyecto:

    def __init__(
        self,
        nombre,
        descripcion,
        fecha_inicio,
        user_id=None
    ):
        self.__user_id = user_id
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio

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
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self.__descripcion = valor

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor):
        self.__fecha_inicio = valor

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"Nombre: {self.nombre} | "
            f"Descripción: {self.descripcion} | "
            f"Fecha inicio: {self.fecha_inicio}"
        )
