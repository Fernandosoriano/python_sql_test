from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
conexion = MySQL(app)

@app.route('/libros', methods=['GET'])
def listar_cursos() -> dict:
    """Función que lista todos los libros
    disponibles en la base de datos

    Returns:
        _type_: dict response
    """
    try:
        cursor = conexion.connection.cursor()
        sql:str = "SELECT id, Nombre, Autor, Editorial FROM libros ORDER BY id ASC"
        cursor.execute(sql)
        datos:tuple = cursor.fetchall()
        libros:list = []
        for libro in datos:
            libro:dict = {'id':libro[0],'nombre': libro[1], 'autor': libro[2], 'editorial': libro[3]}
            libros.append(libro)
        return  make_response(jsonify({'libros': libros, 
                                        'mensaje': "Listado de todos los libros",\
                                        }), 200) 
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'err': ex})
# =====================obtencion de un libro por id, lo uso paara validar post, delete y get uno==========
def leer_libro_bd(id:int):
    """función para leer un libro de la BD
    filtrado por id

    Args:
        id (int): id,de tipo int, para filtar en bd

    Raises:
        ex: _description_

    Returns:
        _type_: _description_
    """
    try:
        cursor = conexion.connection.cursor()
        sql:str = f'SELECT Nombre, Autor, Editorial FROM libros WHERE id = {id}'
        cursor.execute(sql)
        datos:tuple = cursor.fetchone()
        if datos != None:
            libro:dict = {'libro': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
            return libro
        else:
            return None
    except Exception as ex:
        raise ex
# ============================================================================

@app.route('/libros/<id>', methods=['GET'])
def leer_libro(id:int):
    """función que te devuelve un libro filtrado por id

    Args:
        id (int): id usado para filtrar en bd, recibido como query param

    Returns:
        _type_: dicccionario respuesta
    """
    try:
        libro:dict = leer_libro_bd(id)
        if libro != None:
            return jsonify({'libro': libro, 'mensaje': "Libro encontrado.", \
                }) 
        else:
            return jsonify({'mensaje': "Libro no encontrado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'err': ex})


@app.route('/registro', methods=['POST'])
def registrar_libro():
    try:
        libro = leer_libro_bd(request.json['id'])
        if libro != None:
            return jsonify({'mensaje': "Libro ya existe, no se puede duplicar.",\
                'exito': False})
        else:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO libros (id, Nombre, Autor, Editorial) 
            VALUES ({0},'{1}','{2}', '{3}')""".format(request.json['id'],
                                            request.json['Nombre'],
                                            request.json['Autor'],
                                            request.json['Editorial'])
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de inserción. 
            return jsonify({'mensaje': "Libro registrado con éxito"})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'err': ex})


@app.route('/actualizar/<id>', methods=['PUT'])
def actualizar_libro(id):
    try:
        libro = leer_libro_bd(id)
        if libro != None:
            cursor = conexion.connection.cursor()
            print('ID', request.json['id'])
            sql = """UPDATE libros SET Nombre = '{0}', Autor = '{1}',
            Editorial = '{2}' 
            WHERE id = {3}""".format(request.json['Nombre'],
                request.json['Autor'], request.json['Editorial'], request.json['id'])
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de actualización.
            return jsonify({'mensaje': "Libro actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Libro no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'err': ex})

def pagina_no_encontrada(error):
    return "Página no encontrada", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
