from app.detection.box import Box
import cv2, os

percentageSize = 0.1

def dirfor(dir):        #iterate into a directory looking for every jpg file
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            if(file.endswith(".jpg")):
                print(f"let's check this image -> {os.path.join(subdir, file)}")
                ImageProcess(os.path.join(subdir, file))

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
        filename_ = os.path.basename(self.urlname).split(".")[0]
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), scaleFactor=1.2, minNeighbors=3, minSize=(30, 30)) 
        faces = filterbysize(faces,(self.image.shape[0] * self.image.shape[1]),verbose=False)  #Filter by Total area relation  
        print(f'\t[INFO] {self.urlname} dimensions. {self.image.shape[1]} x {self.image.shape[0]}')
        print(f'\t[INFO] {len(faces)} selfie detected.')
        Nn=1
        for face in faces:
            urlname_ = f'img/{filename_}_out{str(Nn)}_faces.jpg'
            print(f'\t[INFO] {urlname_} is goning to be save.',end='  ')
            print(f'selfie dimension : {str(face.get_points())}',end=' -> ')
            cv2.rectangle(self.image, face.get_sPoint(), face.get_ePoint(), (0, 255, 0), 5)
            face.get_amplify(125)
            cv2.rectangle(self.image, face.get_sPoint(), face.get_ePoint(), (255, 0, 0), 5)
            roi_color = self.image[face.yi : face.yf, face.xi : face.xf]       # Select just the selfie area
            # print(f'\t\t [TEST] {str(roi_color)}')
            if len(roi_color) > 0:
                cv2.imwrite(urlname_, roi_color)
                print('[SUCCESS]')
            else:
                print(f'[ERROR] {urlname_} image couldnt process.')
            Nn += 1
        cv2.imwrite('faces_detected.jpg', self.image)
        