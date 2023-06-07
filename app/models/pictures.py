from app.detection.facedetetion import DetectingFaces_OP
from app.models.background import Background
from app.models.colors import Color, Colors
from typing import Optional
from PIL import Image
from rembg import remove
import os
import logging

class Picture(): 
    _verbose = False
    def __init__(self,url: Optional[str]=None, verbose = False) -> None:
        Picture._verbose=verbose
        logging.basicConfig(level=logging.INFO)
        if os.path.isfile(url) and (url.lower().endswith('.jpg') or url.lower().endswith('.png')):
            logging.info(f'[Picture] init {url}')
            self._url=url
        else:
            logging.error(f'[Picture] Sorry "{url}" is not an Image file (jpg or png)')
            self._url=None

    def get_url(self):
        return self._url
    
    def save(self,url:str):
        pass

class BigPic(Picture):
    def get_faces(self):    #Metodo to indentify and get Faces of the big Pic
        if self._url is None:
            logging.error('[BigPic] Sorry there is not a pic')
            return None
        
        # Get faces as a list of PIL images
        faces = DetectingFaces_OP(file=self._url).get_PIL_faces()   
        logging.info(f'[BigPic] {len(faces)} faces detected')        
        #convert to isntancias of FacePic model        
        return [FacePic(img=face) for face in faces]
        

class FacePic(Picture):
    def __init__(self, url: Optional[str]=None, img=None ) -> None:
        logging.info(f'[FacePic]init objeto FacePic url {url}')
        if url is not None: 
            super().__init__(url)
        if img is not None:
            self.pil_image= img
        else:
            # if Picture._verbose: print('[ERROR][FacePic]init empty objeto')
            logging.error('[FacePic]init empty objeto')

    def show(self):
        self.pil_image.show()

    def removeBG(self):
        logging.info("[FacePic]removeBG Let's remove background")
        self.pil_image=remove(self.pil_image)

    def addBGPalette(self, colors: Colors):
        """Take the two color to make the backgorund"""
        self.addBG(colors.value[0], colors.value[1])

    def addBG(self, colorTop: Color, colorBottom: Color):
        logging.info(f"[FacePic]addBG Let's add some background {self.pil_image.size}")
        back = Background(self.pil_image.size)
        # back.set_back_gradientV(colorTop,colorBottom,0.1)
        back.set_back_gradientC(colorTop,colorBottom, 0.3, 0.95)
        # back.set_contorno()
        merged_image = Image.alpha_composite(back.getBackground(), self.pil_image)
        merged_image.show()
