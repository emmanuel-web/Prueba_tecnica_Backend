from  flask import Flask,request, jsonify
from flask_mysqldb import  MySQL
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'pruebatecnica'

mysql = MySQL(app)

@app.route('/clientes', methods=['POST'])
def crear_cliente():
    try:

        nombre = request.json['nombre']
        direccion = request.json['direccion']
        telefono = request.json['telefono']
        nacionalidad = request.json['nacionalidad']
        correo = request.json['correo']

        if not all(len(s.strip()) > 0 for s in [nombre, direccion, telefono, nacionalidad, correo]):
            return jsonify({'mensaje':'por favor ingrese todos los datos'})
    
        cur = mysql.connection.cursor()
        cur.execute(("SELECT * FROM cliente WHERE nombre = '{0}' ".format(nombre)))
        rv = cur.fetchone()
        if  rv:
            return jsonify({'mensaje':'ya existe un suario con este mismo nombre'}),400
        
        query = ("INSERT INTO cliente( nombre, direccion, telefono,nacionalidad, correo) VALUES (%s,%s,%s,%s,%s)")
        Values = (nombre,direccion,telefono,nacionalidad,correo)
        cur.execute(query,Values)
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Cliente creado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})



@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cliente")
        rv = cur.fetchall()
        clientes=[]
        for fila in rv:
            cliente={'Codigo':fila[0],'nombre':fila[1],'direccion':fila[2],'telefono':fila[3],'nacionalidad':fila[4],'correo':fila[5]}
            clientes.append(cliente)
        return jsonify({'clientes':clientes,'mensaje':'lista de clientes'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})
    
    
@app.route('/cliente/<int:cliente_id>', methods=['GET'])
def obtener_cliente(cliente_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(("SELECT * FROM cliente WHERE id = '{0}' ".format(cliente_id)))
        rv = cur.fetchone()
        clientes=[]
        if not rv:
            return jsonify({'mensaje':'no existe el cliente'}),400
            
        for fila in rv:
            cliente={'Codigo':fila[0],'nombre':fila[1],'direccion':fila[2],'telefono':fila[3],'nacionalidad':fila[4],'correo':fila[5]}
            clientes.append(cliente)
        return jsonify({'cliente':clientes,'mensaje':'cliente'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'}) 


@app.route('/clientes/<int:cliente_id>', methods=['PUT'])
def listarCliente(cliente_id):
    try:

        nombre = request.json['nombre']
        direccion = request.json['direccion']
        telefono = request.json['telefono']
        nacionalidad = request.json['nacionalidad']
        correo = request.json['correo']
        cur = mysql.connection.cursor()
        cur.execute(("SELECT * FROM cliente WHERE id = '{0}' ".format(cliente_id)))
        rv = cur.fetchone()
        if not rv:
            return jsonify({'mensaje':'no existe el cliente'}),400

        cur.execute("UPDATE cliente SET nombre='{0}',direccion='{1}',nacionalidad='{2}',telefono='{3}',correo='{4}' WHERE id='{5}'".format(nombre,direccion,nacionalidad,telefono,correo,cliente_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Cliente Actulaizado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})


@app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def eliminarCliente(cliente_id):
    try:

        cur = mysql.connection.cursor()
        cur.execute(("SELECT * FROM cliente WHERE id = '{0}' ".format(cliente_id)))
        rv = cur.fetchone()
        if not rv:
            return jsonify({'mensaje':'no existe el cliente'}),400
        
        cur.execute(("DELETE  FROM cliente WHERE id = '{0}' ".format(cliente_id)))
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Cliente eliminado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})
    
@app.route('/Cliente/ordenes', methods=['POST'])
def crearOrden():
    try:
        cliente_id = request.json['cliente_id']
        items = request.json['items']

        if not cliente_id or not items:
            return jsonify({'mensaje': 'no pueden estar vacios los campos'}),400
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cliente WHERE id='{0}' ".format(cliente_id))
        cliente = cur.fetchone()
        if not cliente:
            return jsonify({'mensaje': 'El cliente especificado no existe.'}),400
            
        query=("INSERT INTO orden (cliente, fecha, estado) VALUES ( %s, %s, %s)" )
        values=( cliente_id, datetime.now(), 'solicitada')
        cur.execute(query,values)
        orden_id = cur.lastrowid

        for i, item in enumerate(items):
            largo = item.get('largo')
            ancho = item.get('ancho')
            if not largo or not ancho:
                return jsonify({'mensaje': f'El item {i+1} no tiene los datos completos.'}),400
            
            query2=("INSERT INTO ordendetalle (orden_id,consecutivo, largo, ancho) VALUES ( %s,%s, %s, %s)")
            Values2=(orden_id, i+1, largo, ancho)
            cur.execute(query2,Values2)
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensaje': 'Orden creada exitosamente.'})

    
    except Exception as ex:
        return jsonify({'mensaje': 'Error'}),400
    

@app.route('/orden/<int:nro_orden>', methods=['PUT'])
def actualizarEstadoOrden(nro_orden):
    try:

        estado=request.json['estado']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE orden SET estado='{0}' WHERE nro_orden = '{1}'".format(estado,nro_orden) )
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Estado actualizado'})
    
    except Exception as ex:
        return jsonify({'mensaje': 'Error'}),400
    
    
@app.route('/ordenes', methods=['GET'])
def ListarOrdenes():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM orden ")
        rv = cur.fetchall()
        ordenes=[]
        for fila in rv:
            orden={'nro_orden':fila[0],'cliente':fila[1],'fecha':fila[2],'estado':fila[3]}
            ordenes.append(orden)
        return jsonify({'ordenes':ordenes,'mensaje':'lista de ordenes'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'}),400
        


if __name__ == '__name__':
    app.run(debug=True)
    




