from .box import Box
from PIL import Image
import cv2
import os

class DetectingFaces_OP:              #Detecting Faces by OpenCV
    #Settings
    _setting_percentageSize = 0.1
    _setting_scaleFactor=1.2
    _setting_minNeighbors=3
    _setting_minSize=(30, 30)
    _verbose=False
    def __init__(self, file:str, verbose = False) -> None:
        self.urlname = file
        DetectingFaces_OP._verbose=verbose
        self.image = cv2.imread(file)

    def _filterbysize(squares, totalarea, verbose = False): #Filter areas by percentage of area Maybe this will be gone
        if verbose: 
            print(f'Get {len(squares)} faces')
        faces = []
        for square in squares:
            box = Box(square)
            areaPercentage_face = 100 * (box.area)/totalarea     #get percentage of area total
            # if verbose: print(f'area = {areaPercentage_face} %')
            if areaPercentage_face > DetectingFaces_OP._setting_percentageSize:          #if % is more tha 1% is a Face
                faces.append(box)
        if verbose: 
            print(f'Send {len(faces)} faces')
        return faces

    def get_cv2_faces(self):
        return self._run()

    def get_PIL_faces(self):
        return [DetectingFaces_OP._transform_cv2_PIL(face) for face in self._run() ]

    def _run(self):         #Detecting all faces inside of image return a list of cv2 
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), 
                                             scaleFactor= self._setting_scaleFactor, 
                                             minNeighbors= self._setting_minNeighbors, 
                                             minSize= self._setting_minSize) 
        faces = DetectingFaces_OP._filterbysize(faces,(self.image.shape[0] * self.image.shape[1]),verbose=False)  #Filter by Total area relation  
        if self._verbose: print(f'\t[INFO_DetectingFaces_OP] {self.urlname} dimensions. {self.image.shape[1]} x {self.image.shape[0]}')
        if self._verbose: print(f'\t[INFO_DetectingFaces_OP] {len(faces)} selfie detected.')
        img_faces = []
        for face in faces:
            if self._verbose: cv2.rectangle(self.image, face.get_startPoint(), face.get_endPoint(), (0, 255, 0), 5)
            face.get_amplify(125)
            if self._verbose: cv2.rectangle(self.image, face.get_startPoint(), face.get_endPoint(), (255, 0, 0), 5)
            img_faces.append(self.image[face.yi : face.yf, face.xi : face.xf])  # Select just the selfie area
        return img_faces

    def _transform_cv2_PIL(img):                                #TRansform an IMAGE from OpenCV model[] to PIL model
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    def _run_old(self):
        filename_ = os.path.basename(self.urlname).split(".")[0]
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), 
                                             scaleFactor= self._setting_scaleFactor, 
                                             minNeighbors= self._setting_minNeighbors, 
                                             minSize= self._setting_minSize) 
        faces = DetectingFaces_OP._filterbysize(faces,(self.image.shape[0] * self.image.shape[1]),verbose=False)  #Filter by Total area relation  
        if self._verbose: print(f'\t[INFO_DetectingFaces_OP] {self.urlname} dimensions. {self.image.shape[1]} x {self.image.shape[0]}')
        if self._verbose: print(f'\t[INFO_DetectingFaces_OP] {len(faces)} selfie detected.')
        Nn=1
        for face in faces:
            if self._verbose: cv2.rectangle(self.image, face.get_startPoint(), face.get_endPoint(), (0, 255, 0), 5)
            face.get_amplify(125)
            urlname_ = f'img/{filename_}_out{str(Nn)}_faces.jpg'
            print(f'\t[INFO] {urlname_} is goning to be save.',end='  ')
            print(f'selfie dimension : {str(face.get_points())}',end=' -> ')
            if self._verbose: cv2.rectangle(self.image, face.get_startPoint(), face.get_endPoint(), (255, 0, 0), 5)
            roi_color = self.image[face.yi : face.yf, face.xi : face.xf]       # Select just the selfie area
            if len(roi_color) > 0:
                cv2.imwrite(urlname_, roi_color)
                print('[SUCCESS]')
            else:
                print(f'[ERROR] {urlname_} image couldnt process.')
            Nn += 1
        if self._verbose: cv2.imwrite('faces_detected.jpg', self.image)
        return None