from app.detection.facedetetion import DetectingFaces_OP
from app.models.background import Background
from app.models.colors import Color, Colors
from typing import Optional
from PIL import Image
from rembg import remove
import os

class Picture(): 
    _verbose = False
    def __init__(self,url: Optional[str]=None, verbose = False) -> None:
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
    def get_faces(self):    #Metodo to indentify and get Faces of the big Pic
        if self._url is None:
            if Picture._verbose: print(f'[ERROR][BigPic] Sorry there is not a pic')
            return None
        
        if Picture._verbose: print(f'[INFO][BigPic] process to detect Faces expected List of faces')
        faces = DetectingFaces_OP(file=self._url).get_PIL_faces()   # Get faces as a list of PIL images
        return [FacePic(img=face) for face in faces]                #convert to isntancias of FacePic model
        

class FacePic(Picture):
    def __init__(self, url: Optional[str]=None, img=None ) -> None:
        if Picture._verbose: print(f'[INFO][FacePic]init objeto FacePic url {url}')
        if url is not None: super().__init__(url)
        if img is not None:
            self.pil_image= img
        else:
            if Picture._verbose: print(f'[ERROR][FacePic]init empty objeto')

    def show(self):
        self.pil_image.show()

    def removeBG(self):
        if Picture._verbose: print(f"[INFO][FacePic]removeBG Let's remove background")
        self.pil_image=remove(self.pil_image)

    def addBGPalette(self, colors: Colors):
        self.addBG(colors.value[0], colors.value[1])

    def addBG(self, colorTop: Color, colorBottom: Color):
        if Picture._verbose: print(f"[INFO][FacePic]addBG Let's add some background {self.pil_image.size}")
        back = Background(self.pil_image.size)
        # back.set_back_gradientV(colorTop,colorBottom,0.1)
        back.set_back_gradientC(colorTop,colorBottom, 0.3, 0.95)
        # back.set_contorno()
        merged_image = Image.alpha_composite(back.getBackground(), self.pil_image)
        merged_image.show()
