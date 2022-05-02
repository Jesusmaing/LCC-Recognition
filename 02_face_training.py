import cv2
import numpy as np
from PIL import Image
import os
import sys

# Base de datos donde están todas las caras reconocidas...
path = os.path.dirname(sys.argv[0]) + "/dataset"


#Se va a utilizar un clasificador LBPH
#https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b
recognizer = cv2.face.LBPHFaceRecognizer_create()

#Se utiliza un clasificador en cascada para detectar todas las caras que estén contenidas en el dataset
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Agarra todas las fotos de la carpeta dataset 
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # Se convierte a escala de grises para optimizar
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("\n [INFO] Aprendiendo nuevas caras... Este proceso puede tardar minutos, por favor espere...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Se guarda el modelo en root...
recognizer.write('trainer.yml') 
# Se imprime el número de caras entrenadas (registradas)
print("\n [INFO] {0} Caras aprendidas. Saliendo del programa...".format(len(np.unique(ids))))
