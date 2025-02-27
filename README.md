# AppComunicacion
SISTEMA DE COMUNICACIÓN DE EMPRESA 

Enunciado del ejercicio
Desarrolla una aplicación web robusta y completa utilizando Django que permita la gestión de proyectos, tareas, mensajes y la colaboración entre usuarios, con un enfoque en la organización y la comunicación efectiva. La aplicación deberá cumplir con los siguientes requisitos:

Gestión de proyectos:

Los usuarios administradores podrán crear nuevos proyectos, asignándoles un título, una descripción, una fecha de inicio y una fecha de finalización.
Los proyectos podrán ser asignados a uno o varios usuarios.
Gestión de tareas:

Dentro de cada proyecto, los usuarios administradores podrán crear nuevas tareas, asignándoles un título, una descripción, una fecha límite y un estado (pendiente, en progreso, completada).
Las tareas podrán ser asignadas a uno o varios usuarios dentro del proyecto.
Visualización de tareas:

La aplicación mostrará una lista de todas las tareas, ordenadas por fecha límite y proyecto.
Se podrán filtrar las tareas por estado, usuario asignado y proyecto.
Modificación y completación de tareas:

Los usuarios asignados a una tarea podrán modificar su descripción y marcarla como completada.
Los usuarios administradores podrán modificar todos los campos de una tarea, incluyendo su estado y los usuarios asignados.
Mensajes y comentarios:

Los usuarios podrán enviar mensajes a otros usuarios dentro de un proyecto.
Los usuarios podrán dejar comentarios en las tareas para discutir detalles o proporcionar actualizaciones.
Gestión de grupos y roles:

La aplicación deberá permitir la creación y gestión de grupos.
Los usuarios podrán ser asignados a uno o varios grupos dentro de un proyecto.
Se deberán definir roles (administrador, miembro, invitado) con diferentes permisos dentro de cada proyecto.
Notificaciones:

La aplicación deberá enviar notificaciones a los usuarios cuando se les asignen tareas, cuando se modifiquen tareas en las que están involucrados, cuando reciban mensajes o cuando haya nuevos comentarios en las tareas.
Interfaz de usuario:

La aplicación deberá tener una interfaz de usuario intuitiva y bien diseñada. Se recomienda utilizar HTML, CSS y JavaScript para el diseño y la interacción.
Base de datos:

Utiliza PostgreSQL como base de datos para almacenar toda la información.
Modelo de datos:

Define un modelo de datos en Django para representar los proyectos, las tareas, los mensajes, los comentarios, los usuarios y los grupos, incluyendo los campos necesarios y las relaciones entre ellos.
Vistas, URLs y formularios:

Crea las vistas, URLs y formularios necesarios en Django para gestionar todas las funcionalidades de la aplicación.
Autenticación y autorización:

Implementa autenticación de usuarios para que cada usuario tenga su propia cuenta y pueda acceder a la aplicación de forma segura.
Implementa un sistema de autorización basado en roles para controlar el acceso a las diferentes funcionalidades de la aplicación.
Consideraciones adicionales
Puedes utilizar librerías de terceros para mejorar la interfaz de usuario, como Bootstrap o Angular o React.
Asegúrate de validar los datos de entrada de los usuarios para evitar errores y vulnerabilidades de seguridad.
Implementa pruebas unitarias para asegurar la calidad del código.
Entrega
Entrega un documento en formato word con capturas de pantalla comentado paso a paso como se ha desarrollado el programa, y como se distribuye la estructura de directorios, así como lo que se hace en cada uno de los ficheros.

Entrega el código fuente de la aplicación Django, en repositorio de git, incluyendo los modelos, vistas, formularios, templates, archivos de configuración y scripts de prueba. Incluye un archivo README con instrucciones detalladas para la instalación y ejecución de la aplicación, así como una descripción de la arquitectura del proyecto y las decisiones de diseño tomadas.

NOTA: no hay que subir los directorios correspondientes al entorno virtual al repositorio git.

Criterios de evaluación
Funcionalidad de la aplicación (cumplimiento de los requisitos).
Calidad del código (legibilidad, organización, comentarios, pruebas unitarias).
Diseño de la interfaz de usuario (usabilidad, estética).
Uso de buenas prácticas de desarrollo de Django.
Correcta implementación de las relaciones entre los modelos de datos.
Robustez y seguridad de la aplicación.
