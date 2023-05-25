import cv2
import sys

def funtion(file):
    print(f'File location: {file}')
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    ) 
    print(str(faces))
    print("Found {0} Faces!".format(len(faces)))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 5)
    status = cv2.imwrite('faces_detected.jpg', image)
    print ("Image faces_detected.jpg written to filesystem: ",status)

if __name__ == '__main__':
    numberPath = sys.argv[1]
    funtion(f'img/{numberPath}.jpg')