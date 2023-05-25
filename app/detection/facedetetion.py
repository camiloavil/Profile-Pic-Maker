from app.detection.box import Box
import cv2

percentageSize = 0.1

def filterbysize(squares, totalarea, verbose = False):
    if verbose: print(f'Get {len(squares)} faces')
    faces = []
    for square in squares:
        box = Box(square)
        areaPercentage_face = 100 * (box.area)/totalarea     #get percentage of area total
        # if verbose: print(f'area = {areaPercentage_face} %')
        if areaPercentage_face > percentageSize:          #if % is more tha 1% is a Face
            faces.append(box)
    if verbose: print(f'Send {len(faces)} faces')
    return faces

class ImageProcess:
    def __init__(self, file:str) -> None:
        self.urlname = file
        self.image = cv2.imread(file)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), scaleFactor=1.2, minNeighbors=3, minSize=(30, 30)) 
        faces = filterbysize(faces,(self.image.shape[0] * self.image.shape[1]),verbose=False)  #Filter by Total area relation  
        Nn=1
        for face in faces:
            # cv2.rectangle(self.image, face.get_sPoint(), face.get_ePoint(), (0, 255, 0), 5)
            face.get_amplify(125)
            # cv2.rectangle(self.image, face.get_sPoint(), face.get_ePoint(), (255, 0, 0), 5)
            # roi_color = self.image[y:y + h, x:x + w]
            roi_color = self.image[face.yi : face.yf, face.xi : face.xf]
            print("[INFO] Object found. Saving locally.")
            cv2.imwrite(f'img/Out{str(Nn)}_faces.jpg', roi_color)
            Nn += 1
        cv2.imwrite('faces_detected.jpg', self.image)