BITACORA USO DE IA 

1. SITUACION 

Durante el desarrolo de EcoTech tuve la duda de como debia funcionar la creacion de cuentas de empleados. No sabia si al crear una cuenta de tipo empleado tambien se debia registrar automaticamente en la tabla EMPLEADO, o si ambos procesos debian ser independientes, en caso de ser automatico o relacionados entre sí, tampoco sabia como conectar la cuenta empleado con los registros del empleado en la tabla. Por lo tanto, decidi usar la inteligencia artificial para que me ayudara a resolver esta duda.

2. PROMPT

"Estoy desarrollando un sistema de gestion para una empresa ficticia llamada EcoTech. El sistema consiste en un software de gestion para la empresa, en este software se pueden crear cuentas de empleados y tambien tiene una base de datos con una tabla para empleados, mi duda es, al crear una cuenta de tipo empleado, ¿deberia registrarse automaticamente en la tabla EMPLEADO o ambos procesos deberian ser independientes? En caso de que sea automatico o relacionado entre sí, ¿como puedo conectar la cuenta empleado con los registros del empleado en la tabla?"

3. RESPUESTA DE LA IA

La IA recomendó mantener ambos procesos separados:

    1. El administrador registra primero al empleado en la tabla empleado.
    2. Posteriormente, crea su cuenta de acceso en la tabla usuarios.
    3. Ambas tablas se relacionan mediante el campo empleado_id, que        referencia la clave primaria user_id de la tabla empleado.
    4. Las cuentas de administrador pueden mantener empleado_id vacío, ya que no necesitan estar asociadas a un empleado.

Esta alternativa permite evitar registros duplicados y mantener organizada la información de acceso y los datos laborales.

4. CODIGO PROPUESTO IMPLEMENTADO 

Se incorporó la propuesta en DAO/GestionUsuario.py, principalmente mediante las siguientes funciones:

    - registrar_usuario(): crea la cuenta del empleado, valida que exista previamente y guarda su identificador en empleado_id. También almacena la contraseña utilizando bcrypt.

    - iniciar_sesion(): valida las credenciales y recupera el rol y el empleado_id asociado a la cuenta.

Se aceptó esta solución porque permitía mantener ambas entidades relacionadas y utilizar esa asociación para controlar los permisos y las funcionalidades disponibles para cada empleado.

se implementó y probé correctamente la creación de empleados y sus respectivas cuentas de acceso, me asegure ademas, de que no se pudieran crear cuentas de empleados sin que existiera un registro previo en la tabla EMPLEADO, y que los permisos y roles se asignaran correctamente según el tipo de cuenta creada.