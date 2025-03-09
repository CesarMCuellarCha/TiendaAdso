from flask import Flask
import pymysql as mysql

# crear el objeto de tipo Flask
app = Flask(__name__)

#configurar carpeta donde se van a guardar las fotos de los productos
app.config["UPLOAD_FOLDER"]="./static/imagenes/"

#variables para conectarse a mysql
host="localhost"
user="root"
password=""
baseDatos="tienda"

#obtener objeto conexión de tipo mysql
miConexion=mysql.connect(host=host, user=user, 
                         password=password, database=baseDatos)


#arrancar la aplicación
if __name__ == '__main__':
    #importar el controlador de producto
    from controladores.productoController import *
    app.run(port=5000, debug=True)
   