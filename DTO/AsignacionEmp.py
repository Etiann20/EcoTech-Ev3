
class AsignacionEmp:

    def __init__(
        self,
        empleado_id,
        proyecto_id,
        rol,
        asignacion_id=None
    ):
        self.__asignacion_id = asignacion_id
        self.__empleado_id = empleado_id
        self.__proyecto_id = proyecto_id
        self.__rol = rol

    @property
    def asignacion_id(self):
        return self.__asignacion_id

    @asignacion_id.setter
    def asignacion_id(self, valor):
        self.__asignacion_id = valor

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
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, valor):
        self.__rol = valor

    def __str__(self):
        return (
            f"ID Asignación: {self.asignacion_id} | "
            f"Empleado: {self.empleado_id} | "
            f"Proyecto: {self.proyecto_id} | "
            f"Rol: {self.rol}"
        )
