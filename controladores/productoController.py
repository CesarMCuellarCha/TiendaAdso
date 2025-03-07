from flask import Flask, render_template, jsonify, request, redirect
import pymysql as mysql
from app import app
from werkzeug.utils import secure_filename
import os

host="localhost"
user="root"
password=""
baseDatos="tienda"

miConexion=mysql.connect(host=host, user=user, password=password, database=baseDatos)


@app.route("/")
def inicio():
    try:
        productos=None
        consulta="select * from productos"
        cursor = miConexion.cursor()
        cursor.execute(consulta)
        productos = cursor.fetchall()               
    except miConexion.Error as error:
        mensaje=str(error)
    return render_template("listarProductos.html", listaproductos=productos)

@app.route("/agregar", methods=['GET','POST'])
def agregar():
    producto=None
    if request.method=='GET':
        return render_template("frmAgregar.html", producto=producto)
    elif(request.method=='POST'):        
        codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])
        categoria = request.form['cbCategoria']
        foto = request.files['fileFoto']
        nombreArchivo = secure_filename(foto.filename)
        listaNombreArchivo = nombreArchivo.rsplit('.', 1)
        extension = listaNombreArchivo[1].lower()
        nuevoNombre = str(codigo) + "." + extension
        rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre)
        try:
            producto = (codigo,nombre,precio,categoria,rutaFoto)
            cursor = miConexion.cursor()
            consulta="insert into productos values(null, %s, %s, %s, %s,%s)"
            cursor.execute(consulta, producto)
            miConexion.commit()
            if cursor.rowcount==1:
                #subimos la foto del producto al servidor
                foto.save(rutaFoto)
                return redirect("/")            
        except miConexion.Error as error:
            miConexion.rollback()
            mensaje="Ya existe producto con ese código"
            return render_template("frmAgregar.html",producto=producto, mensaje=mensaje) 


@app.route("/editar/<int:id>", methods=['GET','POST'])
def editar(id):
    if request.method=="GET":
        try:
            datos=(id,)
            cursor=miConexion.cursor()
            consulta="select * from productos where idProducto=%s"
            cursor.execute(consulta,datos)
            producto = cursor.fetchone()
            if(producto):
                return render_template("frmEditar.html", producto=producto)
        except miConexion.Error as error:
            mensaje="Problemas de conexión a la base de datos"
            return render_template("frmEditar.html", producto=producto, mensaje=mensaje)
    elif(request.method=='POST'):
        pass