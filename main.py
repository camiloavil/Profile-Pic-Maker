import cv2
import sys

def funtion(file):
    print(f'File location: {file}')
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(30, 30)
    ) 
    areaImg = image.shape[0] * image.shape[1]
    print("Área total de la imagen:", areaImg)
    print(type(faces))
    print(str(faces))
    print("Found {0} Faces!".format(len(faces)))
    realfaces = []
    for (x, y, w, h) in faces:
        areaPercentage_face = 100 * (w * h)/areaImg
        if areaPercentage_face > 1:
            print(f'area Face -> {w * h} - {areaPercentage_face} %')
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 5)
            roi_color = image[y:y + h, x:x + w]
            print("[INFO] Object found. Saving locally.")
            cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)


    status = cv2.imwrite('faces_detected.jpg', image)
    print ("Image faces_detected.jpg written to filesystem: ",status)

if __name__ == '__main__':
    numberPath = sys.argv[1]
    funtion(f'img/{numberPath}.jpg')