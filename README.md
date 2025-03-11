# Desarrollo Aplicación Web en Python con Flask y Mysql

El Proyecto realiza las tareas del crud a una base de datos tipo mysql que contiene una tabla llamada productos.
**Las tareas son las siguientes:**
- Listar los productos que se encuentran en la base de datos
- Agregar un producto a la base de datos
- Consultar un producto
- Editar un producto
- Eliminar un producto

Como es una aplicación web se está utilizando el frameword **Flask**, y para la conexión a la base de datos mysql, se está utilizando la librería **Pymysql**.

Se creó una estructura de carpetas de acuerdo a las recomendaciones de **Flask** donde se cuenta con una carpeta **static** para archivos estáticos
y una carpeta **templates** para guardar los archivos html. Adicionalmente a esas carpetas se creó una carpeta llamada **controladores** para aquí crear el archivo controlador
que va a contener las rutas con las funciones de las peticiones que realiza el cliente.

Como parte del ejercicio se creó un **entorno virtual de desarrollo** mediante el comando **python -m venv entorno** para trabajar en dicho entorno. En el entorno se instalaron
las librerías necesarias para la ejecución del mismo como **Flask y Pymysql**.

El proyecto contiene un archivo requirements.txt que contiene el nombre de las librerías utilizadas en el proyecto. Para instalarlo y poner a funcionar el proyecto deben
instalar las librerias que se encuentran en el archivo requirements.txt, ya sea en un entorno nuevo de desarrollo o en el que tengan instalado en los equipos.

También se anexa [material de apoyo]( https://github.com/CesarMCuellarCha/TiendaAdso/blob/master/Material%20Apoyo%20Crud%20python%20mysql.pdf) en documento en formato pdf. 

