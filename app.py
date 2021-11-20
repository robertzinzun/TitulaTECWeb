from flask import Flask,render_template,request,flash,redirect,url_for
from flask_bootstrap import Bootstrap
import requests
app=Flask(__name__)
Bootstrap(app)
app.secret_key='Cl4v3'
@app.route('/')
def inicio():
    return 'App Web de TitulaTEC'

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
    print(nombre+":"+descripcion)
    dict_opcion={"nombre":nombre,"descripcion":descripcion}
    resp=requests.post(url,json=dict_opcion)
    o_json=resp.json()
    flash(o_json['mensaje'])
    return render_template('nuevaOpcion.html')

@app.route('/opciones/ver/<int:id>')
def consultarOpcion(id):
    url = 'http://172.16.1.135:8000/opciones/'+str(id)
    resp=requests.get(url)
    print(resp.json())
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

if __name__=='__main__':
    app.run(debug=True)
