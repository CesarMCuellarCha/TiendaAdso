from flask import Flask

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]="./static/imagenes/"


if __name__ == '__main__':
    from controladores.productoController import *
    app.run(port=5000, debug=True)
   