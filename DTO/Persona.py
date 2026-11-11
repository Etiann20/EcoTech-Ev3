
class Persona:

    def __init__(
        self,
        run,
        nombre,
        direccion,
        telefono,
        correo,
        user_id=None
    ):
        self.__user_id = user_id
        self.__run = run
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.correo = correo 

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, valor):
        self.__user_id = valor

    @property
    def run(self):
        return self.__run

    @run.setter
    def run(self, valor):
        self.__run = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = valor

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"RUN: {self.run} | "
            f"Nombre: {self.nombre} | "
            f"Dirección: {self.direccion} | "
            f"Teléfono: {self.telefono} | "
            f"Correo: {self.correo}"
        )
