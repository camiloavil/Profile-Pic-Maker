from app.detection.facedetetion import DetectingFaces_OP
from PIL import Image
import cv2
import os

class Picture(): 
    _verbose = False
    def __init__(self,url: str, verbose = False) -> None:
        Picture._verbose=verbose
        if os.path.isfile(url) and (url.lower().endswith('.jpg') or url.lower().endswith('.png')):
            if Picture._verbose: print(f'[INFO][Picture] init {url} picture')
            self._url=url
        else:
            if Picture._verbose: print(f'[ERROR][Picture] Sorry "{url}" is not an Image file (jpg or png)')
            self._url=None

    def get_url(self):
        return self._url
    
    def save(self,url:str):
        pass

class BigPic(Picture):
    def get_faces(self):
        if self._url is None:
            if Picture._verbose: print(f'[ERROR][BigPic] Sorry there is not a pic')
            return None
        
        if Picture._verbose: print(f'[INFO][BigPic] process to detect Faces expected List of faces')
        faces = DetectingFaces_OP(file=self._url).get_PIL_faces()
        print(faces)
        faces = [FacePic(face) for face in faces]
        print(faces)
        # face = faces[0]
        # imagen_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        # # Crear el objeto Image desde la imagen RGB
        # imagen_pil = Image.fromarray(imagen_rgb)
        # imagen_pil.show()
        return None

class FacePic(Picture):
    def __init__(self, url: str, img: Image) -> None:
        if Picture._verbose: print(f'[INFO][FacePic] init objeto FacePic')
        super().__init__(url)
        self.pil_image= img
