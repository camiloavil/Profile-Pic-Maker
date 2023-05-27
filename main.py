from app.detection.box import Box
from app.detection.facedetetion import scaning_dir, filterbysize
import cv2
import sys, os

def funtion(file):
    print(f'File location: {file}')
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=3,
        minSize=(30, 30)
    )
    faces = filterbysize(faces,(image.shape[0] * image.shape[1]),verbose=True)  #Filter by Total area relation
    new_faces = []
    # check intersections
    for i in range(len(faces)):
        for j in range(i + 1,len(faces)):
            if faces[i].intercepts(faces[j]) is False:
                new_faces.append(faces[i])
            # print(f'{i} con {j}')
            # print(f'Intercepcion ',faces[i].intercepts(faces[j]))
    print(faces)
    for face in faces:
        print (f'S point {face.get_sPoint()} E point {face.get_ePoint()}')
        cv2.rectangle(image, face.get_sPoint(), face.get_ePoint(), (0, 255, 0), 5)
        face.get_amplify(125)
        print (f'S point {face.get_sPoint()} E point {face.get_ePoint()}')
        cv2.rectangle(image, face.get_sPoint(), face.get_ePoint(), (255, 0, 0), 5)
        print('\n')
    status = cv2.imwrite('faces_detected.jpg', image)
    print ("Image faces_detected.jpg written to filesystem: ",status)


if __name__ == '__main__':
    # numberPath = sys.argv[1]
    scaning_dir(f'img/input/', testing=False)