from app.detection.box import Box
import cv2, os

percentageSize = 0.1

def scaning_dir(dir, testing = False):        #iterate into a directory looking for every jpg file
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            if(file.endswith(".jpg")):
                print(f"let's check this image -> {os.path.join(subdir, file)}")
                ImageProcess(os.path.join(subdir, file), testing)


class DetectingFaces_OP:              #Detecting Faces by OpenCV
    #Settings
    _setting_scaleFactor=1.2
    _setting_minNeighbors=3
    _setting_minSize=(30, 30)
    _debug=False
    def __init__(self, file:str, debug = False) -> None:
        self.urlname = file
        DetectingFaces_OP._debug=debug
        self.image = cv2.imread(file)

    def filterbysize(squares, totalarea, verbose = False): #Filter areas by percentage of area Maybe this will be gone
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
    
    def _run(self):
        filename_ = os.path.basename(self.urlname).split(".")[0]
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), 
                                             scaleFactor= self._setting_scaleFactor, 
                                             minNeighbors= self._setting_minNeighbors, 
                                             minSize= self._setting_minSize) 
        faces = DetectingFaces_OP.filterbysize(faces,(self.image.shape[0] * self.image.shape[1]),verbose=False)  #Filter by Total area relation  
        if self._debug: print(f'\t[INFO_DetectingFaces_OP] {self.urlname} dimensions. {self.image.shape[1]} x {self.image.shape[0]}')
        if self._debug: print(f'\t[INFO_DetectingFaces_OP] {len(faces)} selfie detected.')
        Nn=1
        for face in faces:
            if self._debug: cv2.rectangle(self.image, face.get_startPoint(), face.get_endPoint(), (0, 255, 0), 5)
            face.get_amplify(125)
            urlname_ = f'img/{filename_}_out{str(Nn)}_faces.jpg'
            print(f'\t[INFO] {urlname_} is goning to be save.',end='  ')
            print(f'selfie dimension : {str(face.get_points())}',end=' -> ')
            if self._debug: cv2.rectangle(self.image, face.get_startPoint(), face.get_endPoint(), (255, 0, 0), 5)
            roi_color = self.image[face.yi : face.yf, face.xi : face.xf]       # Select just the selfie area
            if len(roi_color) > 0:
                cv2.imwrite(urlname_, roi_color)
                print('[SUCCESS]')
            else:
                print(f'[ERROR] {urlname_} image couldnt process.')
            Nn += 1
        if self._debug: cv2.imwrite('faces_detected.jpg', self.image)

        return None