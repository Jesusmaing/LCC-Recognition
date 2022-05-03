import cv2
import os
import sys

#--------------------Carpetas donde se almacenará el entramiento---------------------
dir_path = os.path.dirname(sys.argv[0]) + "/dataset"

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

face_id = input('\n Ingresa la matricula del alumno y presiona ENTER: ')

   
#Generamos más 10x fotos más, es decir... si se toman 100 fotos, vamos a generar 1000 fotos de un rostro. 
def generate_more_photos():
    imagePaths = [os.path.join(dir_path,f) for f in os.listdir(dir_path) if f.split('.')[1] == face_id] 
    count = len(imagePaths)

    for imagePath in imagePaths:
        #print(imagePath)
        img = cv2.imread(imagePath)
        
        #FLIP IMAGES
        for i in range(-1,2):
            count+=1
            cv2.imwrite(("{}/User." + str(face_id) + '.' + str(count) + "flipped.jpg").format(dir_path), cv2.flip(img, i))
        
        #RESIZE IMAGES
        # generate Gaussian pyramid for A
        A = img
        G = A.copy()
        for i in range(6):
            G = cv2.pyrDown(G)
            count+=1
            cv2.imwrite(("{}/User." + str(face_id) + '.' + str(count) + "resized.jpg").format(dir_path), G)
        # generate Laplacian Pyramid for A
           
cam = cv2.VideoCapture(0)
#Asignamos un tamaño para las fotos 
cam.set(3, 640) 
cam.set(4, 480)

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id

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
cam.release()
cv2.destroyAllWindows()
print("\n [INFO] El programa terminó de capturar tu cara...")
print("\n [INFO] Ya te puedes levantar... Ahora, convertirá esas fotos en más fotos..")


generate_more_photos()

print("\n [INFO] El programa ha terminado correctamente!..")





