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

class Bigpic(Picture):
    def get_faces(self):
        if self._url is None:
            if Picture._verbose: print(f'[ERROR][Bigpic] Sorry there is not a pic')
            return None
        
        if Picture._verbose: print(f'[INFO][Bigpic] process to detect Faces expected List of faces')
        faces = DetectingFaces_OP(file=self._url).get_PIL_faces()
        print(faces)
        # face = faces[0]
        # imagen_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        # # Crear el objeto Image desde la imagen RGB
        # imagen_pil = Image.fromarray(imagen_rgb)
        # imagen_pil.show()
        return None

class FacePic(Picture):
    def __init__(self, url: str, img: Image) -> None:
        super().__init__(url)
        self.pil_image= img

    def save(self,url:str):
        pass