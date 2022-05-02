import cv2
import os
import sys

#--------------------Carpetas donde se almacenará el entramiento---------------------
dir_path = os.path.dirname(sys.argv[0]) + "/dataset"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    
    
cam = cv2.VideoCapture(0)
#Asignamos un tamaño para las fotos 
cam.set(3, 640) 
cam.set(4, 480)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n Ingresa la matricula del alumno y presiona ENTER')

print("\n [INFO] Iniciando la sesión de fotos hacía tu cara... Mira a la cámara y sonrie :)  ...")

count = 0

while(True):

    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        #Se guardan las fotos en la carpeta dataset
        cv2.imwrite(("{}/User." + str(face_id) + '.' + str(count) + ".jpg").format(dir_path), gray[y:y+h,x:x+w])

        cv2.imshow('Imagenes', img)

    k = cv2.waitKey(100) & 0xff # Presiona ESC para salir del programa
    if k == 27:
        break
    elif count >= 200: # Proceso de 200 fotos...
         break

# Do a bit of cleanup
print("\n [INFO] Saliendo del programa y limpiando memoria...")
cam.release()
cv2.destroyAllWindows()


