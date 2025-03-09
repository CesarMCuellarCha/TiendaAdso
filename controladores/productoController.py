from flask import Flask, render_template, jsonify, request, redirect
#importar objetos del archivo app.py
from app import app, miConexion 
#libreria para obtener nombre de archivo
from werkzeug.utils import secure_filename 
#libreria para guardar archivos en servidor
import os


@app.route("/")
def inicio():
    """_summary_
        Obtiene todos los productos de la base de datos
        y los retorna a la vista listarProductos
    Returns:
        _type_: Tupla de Tuplas, con los productos
    """
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
    """_summary_
        Recibe peticiones del front-end de tipo GET y
        Post para agregar un Producto a la base de datos.
        Cuando es GET muestra el formulario y cuando es 
        POST recibe los datos del formulario para
        agregar el producto
    Returns:
        _type_: Si se agrega bien el producto, redirecciona
        a la ruta "/" y sino retorna a la vista de 
        agregar el producto con una tupla (producto) con el producto
        para poder visualizar lo que se había ingresado
        en el formulario.
    """
    producto=None
    if request.method=='GET':
        return render_template("frmAgregar.html", producto=producto)
    elif(request.method=='POST'):  
        #obtener los datos que vienen del formulario      
        codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])
        categoria = request.form['cbCategoria']
        foto = request.files['fileFoto']
        #obtener el nombre del campo de tipo file
        nombreArchivo = secure_filename(foto.filename)
        listaNombreArchivo = nombreArchivo.rsplit('.', 1)
        #crear la extensión del archivo en minúscula
        extension = listaNombreArchivo[1].lower()
        #crear el nombre del archivo como se va a guardar en el servidor
        # se utiliza codigo.extensión, ya que el código no se repite
        nuevoNombre = str(codigo) + "." + extension
        rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre)
        try:
            producto = (codigo,nombre,precio,nuevoNombre,categoria)
            cursor = miConexion.cursor()
            consulta="insert into productos values(null, %s, %s, %s, %s,%s)"
            cursor.execute(consulta, producto)
            miConexion.commit()
            if cursor.rowcount==1:               
                foto.save(rutaFoto) #subimos la foto del producto al servidor
                return redirect("/")            
        except miConexion.Error as error:
            miConexion.rollback()
            mensaje="Ya existe producto con ese código"
            return render_template("frmAgregar.html",producto=producto, mensaje=mensaje) 


@app.route("/editar/<int:id>", methods=['GET','POST'])
def editar(id):
    """_summary_
        Recibe una petición de Tipo GET o POST del 
        front-end para editar un producto de acuerdo
        a su id, el cual lo recibe en la url. Si es
        de Tipo GET lo consulta y lo retorna a la vista
        que permite editar el producto. Si la Petición
        es de tipo POST recibe de la vista los datos
        del producto para ser actualizado
    Args:
        id (_type_): int, id del producto

    Returns:
        _type_: LO redirecciona  a la vista inicial "/"
        si se actualiza bien, de lo contrario retorna a
        la misma vista con el producto para ser visualizado
        y con un mensaje informando el error.
    """
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
        mensaje=None
        codigo = int(request.form['txtCodigo'])
        nombre = request.form['txtNombre']
        precio = int(request.form['txtPrecio'])
        categoria = request.form['cbCategoria']
        foto = request.files['fileFoto']
        nombreArchivo = secure_filename(foto.filename)       
        try:
            cursor = miConexion.cursor()
            #si no llega nada en foto no se actualiza el campo de la foto
            if nombreArchivo == "":
                #tupla con los datos del producto
                producto = (codigo,nombre,precio,categoria, id)
                consulta = "update productos set proCodigo=%s, proNombre=%s, \
                proPrecio=%s, proCategoria=%s where idProducto=%s"                
                cursor.execute(consulta, producto)
                miConexion.commit() 
                if cursor.rowcount==1:
                    return redirect("/")
                else:
                    mensaje="Problemas al actualizar sin foto"
            else:
                #se actualiza el campo foto
                listaNombreArchivo = nombreArchivo.rsplit('.', 1)
                extension = listaNombreArchivo[1].lower()
                nuevoNombre = str(codigo) + "." + extension
                #tupla con los datos del producto a actualizar
                producto = (codigo,nombre,precio,categoria,nuevoNombre, id)
                rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre)
                consulta = "update productos set proCodigo=%s, proNombre=%s, \
                proPrecio=%s, proCategoria=%s, proFoto=%s where idProducto=%s"
                cursor.execute(consulta, producto)
                miConexion.commit()
                if cursor.rowcount==1:
                    #subimos la foto del producto al servidor
                    foto.save(rutaFoto)
                    return redirect("/")
                else:
                    mensaje="problemas al actualizar con foto"
        except miConexion.Error as error:
            miConexion.rollback()
            mensaje="Problemas al actualizar. Revisar \
            código del producto, puede estar repetido"
        
        #retorno a la misma vista cuando hay problemas al actualizar
        producto=(id, codigo, nombre,precio,nombreArchivo,categoria)              
        return render_template("frmEditar.html",producto=producto, mensaje=mensaje) 
        
@app.route("/eliminar/<int:id>", methods=['GET'])
def eliminar(id):
    """_summary_
        Elimina un  producto de acuerdo a su id que
        recibe mediante petición GET
    Args:
        id (_type_): int, id del producto

    Returns:
        _type_: lo redirecciona a la ruta raiz
    """
    if request.method == 'GET':
        try:
            print("voy a eliminar")
            productoEliminar=(id,)
            cursor = miConexion.cursor()
            #datos para eliminar foto
            consulta="select proFoto from productos where idProducto=%s"
            cursor.execute(consulta,productoEliminar)
            foto=cursor.fetchone()[0] #obtenemos el contenido de la posición 0
            rutaFoto = os.path.join(app.config['UPLOAD_FOLDER'], foto)
            consulta="delete from productos where idProducto=%s"
            cursor.execute(consulta, productoEliminar)
            miConexion.commit()
            if cursor.rowcount == 1:
                #eliminar el archivo fisicamente               
                os.remove(rutaFoto)                
        except miConexion.Error as error:
            miConexion.rollback()
            mensaje="Problemas al eliminar"
            
    return redirect("/")