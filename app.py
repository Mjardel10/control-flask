from flask import Flask, render_template,request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




import requests
import json
import http

 

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'





@app.route('/',methods=["GET"])
def inicio():
    
    #posts=Post.query.order_by(Post.fecha.desc()).all()  #ORM
    res = requests.get('https://api-go-students.herokuapp.com/api/estudiantes')
    data=json.loads(res.text)
    estudiantes=data["data"]

    res = requests.get('https://api-go-students.herokuapp.com/api/cursos')
    data=json.loads(res.text)
    cursos=data["data"]
     
    return render_template("inicio.html",estudiantes=estudiantes,cursos=cursos)


#nos dirige al template de agregar alumno
@app.route('/agregar/alumno',methods=["GET"])
def agregar_alumnos():
    res = requests.get('https://api-go-students.herokuapp.com/api/cursos')
    data=json.loads(res.text)
    cursos=data["data"]

    return render_template("agregar_alumnos.html",cursos=cursos)


#nos dirige al template de agregar curso
@app.route('/agregar/curso')
def agregar_curso():
    return render_template("agregar_cursos.html")



#url que obtiene los datos de los cursos y los muestra en una grafica
@app.route('/grafica',methods=["GET"])
def grafica():
    req = requests.get('https://api-go-students.herokuapp.com/api/grafica-cursos')
    data=json.loads(req.text)
    cursos=data["data"]
    success=data["success"] 
    total=data["total"]  


    if success!=True:
        flash(u'No se ha podido generar el gráfico',"danger")        
        return redirect("/")
    elif cursos==None:
        flash(u'No hay datos Para generar el gráfico',"danger")        
        return redirect("/")

    nombres=[]
    valores=[]

    for curso in cursos:
        nombres.append(str(curso["curso"]))
        valores.append(curso["cantidad"])
        
    return render_template("grafica.html",total=total,nombres=nombres,valores=valores)



@app.route('/prueba',methods=["GET"])
def prueba():
    res = requests.get('https://api-go-students.herokuapp.com/api/cursos')
    
    data=json.loads(res.text)
    cursos=data["data"]
    

    return render_template("prueba.html", cursos=cursos)



#urls para guardar los datos a la api go
@app.route('/guardar-curso',methods=["POST"])
def guardar_curso():    
    
    nombre=request.form.get("Curso")
    horario=request.form.get("Horario")
    fecha=request.form.get("Fecha_Inicio")
    lugar=nombre_curso=request.form.get("Lugar")
    desc= nombre_curso=request.form.get("Descripcion")
    
    
    res = requests.post('https://api-go-students.herokuapp.com/api/insertar-curso', json={"nombre":nombre, "horario":horario,"fecha_i":fecha,"lugar":lugar,"descripcion":desc})
    print(res.json)

    data=json.loads(res.text)
    success=data["success"]
    if success==True:
        flash(u'Curso Guardado exitosamente',"success")
        return redirect("/agregar/curso")
    else:
        flash(u'El Curso no ha sido Guardado',"danger")
        #return redirect("/agregar/curso")

    #return '', 204     
    return redirect("/agregar/curso")
    



#funcion que llama a la api de go para insertar alumno
@app.route('/guardar-alumno',methods=["POST","GET"])
def guardar_alumno():    
    nombres=request.form.get("Nombres")
    apellidos=request.form.get("Apellidos")
    fecha=request.form.get("Fecha_Nacimiento")
    direccion=nombre_curso=request.form.get("Direccion")
    correo= nombre_curso=request.form.get("Correo")
    id_curso=request.form.get("Curso")


    print(id_curso)
    if int(id_curso)==0:
        flash(u'Debe llenar todos los Campos',"danger")
        print("error")
    else:
        print("hola")
        res = requests.post('https://api-go-students.herokuapp.com/api/insertar-estudiante', json={"nombres":nombres, "apellidos":apellidos,"fecha_n":fecha,"direccion":direccion,"correo":correo,"id_curso":int(id_curso)})
        print(res.json)

    
        data=json.loads(res.text)
        success=data["success"]
        if success==True:
            flash(u'Estudiante Guardado exitosamente',"success")
            return redirect("/agregar/alumno")
        else:
            flash(u'El Estudiante no ha sido Guardado',"danger")
    

    return redirect("/agregar/alumno")


#if __name__=="__main__":
#    app.run(host='127.0.0.9',port=4455,debug=True) 
if __name__=="__main__":
   app.run() 


