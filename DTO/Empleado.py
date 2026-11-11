
from DTO.Persona import Persona


class Empleado(Persona):

    def __init__(
        self,
        run,
        nombre,
        direccion,
        telefono,
        correo,
        fecha_inicio,
        salario,
        departamento_id,
        user_id=None
    ):
        super().__init__(
            run,
            nombre,
            direccion,
            telefono,
            correo,
            user_id
        )

        self.__fecha_inicio = fecha_inicio
        self.__salario = salario
        self.__departamento_id = departamento_id

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor):
        self.__fecha_inicio = valor

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, valor):
        self.__salario = valor

    @property
    def departamento_id(self):
        return self.__departamento_id

    @departamento_id.setter
    def departamento_id(self, valor):
        self.__departamento_id = valor

    def __str__(self):
        return (
            f"ID: {self.user_id} | "
            f"RUN: {self.run} | "
            f"Nombre: {self.nombre} | "
            f"Fecha inicio: {self.fecha_inicio} | "
            f"Salario: {self.salario} | "
            f"Departamento: {self.departamento_id}"
        )
