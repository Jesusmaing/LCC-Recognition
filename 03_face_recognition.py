import cv2
import numpy as np
import os 


#Librerias gráficas para presentar una interfaz de usuario...
from tkinter import *
from tkinter import messagebox, Canvas, simpledialog
from PIL import Image,ImageTk
import imutils

#importamos la libreria para acceder a la base de datos
import pymysql

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

def iniciar():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()
    
def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(0.1*cap.get(3)), int(0.1*cap.get(4))),
            )
            for(x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100 and round(100 - confidence) > 50.0):
                    lcc_matricula.set(id)
                else:
                    lcc_matricula.set(-1)
                    id = "Desconocido"
                confidence =round(100 - confidence)
                
                #Si la coincidencia es mayor al 50%, se muestra la matricula del usuario
                #Esto es para que evite predecir rostros teniendo un porcentaje de acertar
                #muy bajo, por ende, empezaría a arrojar coincidencias muy malas o erroneas.
                if confidence > 50.0:
                    cv2.putText(frame, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                    cv2.putText(frame, str(confidence)+"%", (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
            
            btnIniciar.config(state="disabled")
            btnFinalizar.config(state="normal")
            btnInfo.config(state="normal")
            btnError.config(state="normal")


        else:
            lblVideo.image = ""
            cap.release()
def finalizar():
    global cap
    cap.release()
    lcc_matricula_identificado.set("")
    lcc_nombre_identificado.set("")
    lcc_apellido_identificado.set("")
    lcc_creditos_identificado.set("")
    lcc_kardex_identificado.set("")
    btnIniciar.config(state="normal")
    btnFinalizar.config(state="disabled")
    btnInfo.config(state="disabled")
    btnError.config(state="disabled")
    

def obtenerinfo():
    creditos_totales = 383
    if lcc_matricula.get() == -1:
        messagebox.showinfo(message="No se ha podido reconocer tu rostro, vuelve a intentarlo o registra tu rostro.", title="¡Advertencia!")
        return
    lcc_matricula_identificado.set(lcc_matricula.get())
    db = pymysql.connect(host = 'localhost', 
                         user= 'root',
                         password='xSK!NyF@pU#sD&L', 
                         database='alumnos_lcc',)
    cur = db.cursor()
    sql = 'select * from alumno where idalumno = {}'.format(lcc_matricula_identificado.get())
    cur.execute(sql)
    results = cur.fetchall()
    if not results:
        messagebox.showinfo(message="Tus datos no están capturados correctamente. Contactate con el administrador", title="¡Error!")
        return
    lcc_matricula_identificado.set(results[0][0])
    lcc_nombre_identificado.set(results[0][1])
    lcc_apellido_identificado.set(results[0][2])
    lcc_creditos_identificado.set(str(results[0][3]) + '/{} - {}%'.format(creditos_totales, round(results[0][3]/creditos_totales*100,2) ))
    lcc_kardex_identificado.set(results[0][4])
    if results[0][3] < creditos_totales:
        lcc_sc_identificado.set("Todavía no cumples con el requisito mínimo de 70% de créditos aprobados para solicitar registro como prestador de Servicio Social.")
    if results[0][3] >= creditos_totales:
        lcc_sc_identificado.set("¡Ya puedes aplicar!")
    
    
    
    
def error_dialog():
    s= simpledialog.askstring("Ingresa un número", "¿Cúal es tu matricula?")
    lcc_matricula.set(s)
    obtenerinfo()
    messagebox.showinfo(message="Gracias por reportar. Esto ayudará a que el reconocimiento facial sea más preciso.", title="¡Se agradece!")

#Iniciar Tkinter
cap = None
root = Tk()
background1= Label(root, text="", bg='#3a7ff6', width=100, height=170).place(x=0, y=0)
background2 = Label(root, text="", bg='#ffffff', width=50, height=170).place(x=700, y=0)
root.title('Ciencias de la computación')
root.geometry("1000x600")


#Variables para datos del alumno identificado
lcc_matricula = IntVar()
lcc_matricula_identificado = IntVar()
lcc_nombre_identificado = StringVar()
lcc_apellido_identificado = StringVar()
lcc_creditos_identificado = IntVar()
lcc_kardex_identificado = DoubleVar()
lcc_sc_identificado = StringVar()


#Iniciamos las variables en blanco 
lcc_matricula_identificado.set("")
lcc_nombre_identificado.set("")
lcc_apellido_identificado.set("")
lcc_creditos_identificado.set("")
lcc_kardex_identificado.set("")
lcc_sc_identificado.set("")


#Botones de control
btnIniciar = Button(root, text="Iniciar", width=45, command=iniciar)
btnIniciar.grid(column=0, row=0, padx=5, pady=5)

btnFinalizar = Button(root, text="Finalizar", width=45, command=finalizar, state = DISABLED)
btnFinalizar.grid(column=1, row=0, padx=5, pady=5)

btnInfo = Button(root, text="Obtener información", width=45, height=3, command=obtenerinfo,state = DISABLED )
btnInfo.place(x=150, y=530)

btnError = Button(root, text="¿No eres tu?", width=15, command=error_dialog,state = DISABLED )
btnError.place(x=750, y=550)


#Formulario del alumno reconocido
x_place = 750
y_place = 50

presentacion_info = Label(root, text = 'Datos de la persona', font='Helvetica 14', background="#ffffff").place(x=x_place-40,y=y_place-30)


nombreAlumno_Label = Label(root, text = 'Nombre',  font=("Arial", 12), background="#ffffff").place(x=x_place,y=y_place)
nombreAlumno_Label = Label(root, text = 'Apellido',  font=("Arial", 12), background="#ffffff").place(x=x_place,y=y_place+60)
matriculaAlumno_Label = Label(root, text = 'Matricula',  font=("Arial", 12), background="#ffffff").place(x=x_place,y=y_place+120)
creditosAlumno_Label = Label(root, text = 'Créditos',  font=("Arial", 12), background="#ffffff").place(x=x_place,y=y_place+180)
kardexAlumno_Label = Label(root, text = 'Kardex',  font=("Arial", 12), background="#ffffff").place(x=x_place,y=y_place+240)
ServicioSocialAlumno_Label = Label(root, text = 'Servicio social',  font=("Arial", 12), background="#ffffff").place(x=x_place,y=y_place+300)

nombreAlumno_Output = Label(root, textvariable = lcc_nombre_identificado, font='Helvetica 14 bold', background="#ffffff", justify="center").place(x=x_place-40,y=y_place+20)
apellidoAlumno_Output = Label(root, textvariable = lcc_apellido_identificado,   font='Helvetica 14 bold', background="#ffffff", justify="center").place(x=x_place-40,y=y_place+80)
matriculaAlumno_Output = Label(root, textvariable = lcc_matricula_identificado,  font='Helvetica 14 bold', background="#ffffff" , justify="center").place(x=x_place-40,y=y_place+140)
creditosAlumno_Output = Label(root, textvariable = lcc_creditos_identificado,  font='Helvetica 14 bold', background="#ffffff" , justify="center").place(x=x_place-40,y=y_place+200)
kardexAlumno_Output = Label(root, textvariable = lcc_kardex_identificado, font='Helvetica 14 bold', background="#ffffff", justify="center").place(x=x_place-40,y=y_place+260)
ServicioSocialAlumno_Output = Label(root, textvariable = lcc_sc_identificado,  font=("Arial", 12), background="#ffffff", wraplength=180, justify="center").place(x=x_place-40,y=y_place+320)

#Configuración para Tkinter
lblVideo = Label(root, background="#3a7ff6")
lblVideo.grid(column=0, row=1, columnspan=2)
root.resizable(True, False) 
root.mainloop()

