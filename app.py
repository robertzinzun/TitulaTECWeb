from flask import Flask,render_template,request,flash,redirect,url_for,jsonify
from flask_bootstrap import Bootstrap
from suds.client import Client
import requests
app=Flask(__name__)
Bootstrap(app)
app.secret_key='Cl4v3'
@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/login',methods=['post'])
def login():
    url = 'http://172.16.1.135:8000/alumnos/autenticar'
    email=request.form['email']
    password=request.form['password']
    dict={"email":email,"password":password}
    respuesta=requests.get(url,json=dict)
    salida=respuesta.json()
    estatus=salida['estatus']
    if estatus=='Ok':
        return render_template('principal.html',usuario=salida['alumno'])
    else:
        flash(salida['mensaje'])
        return render_template('login.html')


@app.route('/opciones',methods=['get'])
def consultaOpciones():
    url = 'http://172.16.1.135:8000/opciones'
    respuesta = requests.get(url)
    return render_template('consultaOpciones.html',resp=respuesta.json())

@app.route('/opciones/nueva')
def nuevaOpcion():
    return render_template('nuevaOpcion.html')

@app.route('/opciones/guardar',methods=['post'])
def guardarOpcion():
    url='http://172.16.1.135:8000/opciones'
    nombre=request.form['nombre']
    descripcion=request.form['descripcion']
    dict_opcion={"nombre":nombre,"descripcion":descripcion}
    resp=requests.post(url,json=dict_opcion)
    o_json=resp.json()
    flash(o_json['mensaje'])
    return render_template('nuevaOpcion.html')

@app.route('/opciones/ver/<int:id>')
def consultarOpcion(id):
    url = 'http://172.16.1.135:8000/opciones/'+str(id)
    resp=requests.get(url)
    return render_template('editarOpcion.html',resp=resp.json())

@app.route('/opciones/editar',methods=['POST'])
def editarOpcion():
    id =request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    dict_opcion = {"idOpcion":id,"nombre":nombre,"descripcion":descripcion}
    url = 'http://172.16.1.135:8000/opciones'
    resp=requests.put(url,json=dict_opcion)
    o_json=resp.json()
    flash(o_json['mensaje'])
    return redirect(url_for('consultarOpcion',id=id))

@app.route('/opciones/eliminar/<int:id>')
def eliminarOpcion(id):
    url = 'http://172.16.1.135:8000/opciones/' + str(id)
    resp=requests.delete(url)
    o_json = resp.json()
    flash(o_json['mensaje'])
    return redirect(url_for('consultaOpciones'))

@app.route('/alumnos/nuevo')
def nuevoAlumno():
    return render_template('registroAlumno.html')

@app.route('/alumnos/consultar/<nocontrol>',methods=['get'])
def consultarAlumno(nocontrol):
    url = 'http://172.16.1.125:8080/WSSIE/SIEService?wsdl'
    cliente = Client(url)
    alumno=cliente.service.consultarAlumno(noControl=nocontrol)
    dict={"nombre":alumno.nombreCompleto,"telefono":alumno.telefono,
          "email":alumno.email,"creditos":alumno.creditos,"sexo":alumno.sexo,
          "idCarrera":alumno.idCarrera,"nombreCarrera":alumno.nombreCarrera}
    return jsonify(dict)

@app.route('/alumnos/registrar',methods=['post'])
def registrarAlumno():
    url = 'http://172.16.1.135:8000/alumnos'
    nombre=request.form['nombre']
    sexo=request.form['sexo']
    telefono=request.form['telefono']
    email=request.form['email']
    password=request.form['password']
    nocontrol=request.form['nocontrol']
    anioEgreso=request.form['anio']
    creditos=request.form['creditos']
    idCarrera=request.form['idCarrera']
    dict_alumno={"nombre":nombre,"sexo":sexo,"telefono":telefono,"email":email,
                 "password":password,"nocontrol":nocontrol,"anioEgreso":anioEgreso,
                 "creditos":creditos,"idCarrera":idCarrera}
    resp = requests.post(url,json=dict_alumno)
    o_json = resp.json()
    flash(o_json['mensaje'])
    return redirect(url_for('nuevoAlumno'))

if __name__=='__main__':
    app.run(debug=True)
