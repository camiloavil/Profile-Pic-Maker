from app.detection.facedetetion import DetectingFaces_OP
from app.models.background import Background
from app.models.colors import Color, Colors
from typing import Optional
from PIL import Image, ImageDraw, ImageFilter

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
        """This function removes the th background of the pic using rembg module"""
        logging.info("[FacePic]removeBG Let's remove background")
        self.pil_image=remove(self.pil_image)
    
    def set_contour(self):
        """Set the shape of image Circular for now"""
        radius = 0.95*min(self.pil_image.size) // 2
        self.Cborder=radius
        center_x = self.pil_image.size[0] // 2
        center_y = self.pil_image.size[1] // 2
        mask = Image.new("L", (self.pil_image.size), 0)  # Máscara para el área fuera del círculo
        draw_mask = ImageDraw.Draw(mask)
        # Dibujar círculo en la máscara
        draw_mask.ellipse((center_x - radius, 
                           center_y - radius, 
                           center_x + radius, 
                           center_y + radius), 
                           fill=255)
        # mask.show()
        self.pil_image.putalpha(mask)  # Aplicar la máscara como transparencia
        
    
    def setBlur(self,blur: int):
        # Aplicar filtro de desenfoque gaussiano
        blurred_background = self.pil_image.filter(ImageFilter.GaussianBlur(blur))  
        # Combinar imagen difuminada con la original  
        self.pil_image = Image.alpha_composite(blurred_background, self.pil_image)    
    
    def addBGPalette(self, colors: Colors):
        """Take the two color to make the backgorund"""
        self.addBG(colors.value[0], colors.value[1])

    def addBG(self, colorTop: Color, colorBottom: Color):
        logging.info(f"[FacePic]addBG Let's add some background {self.pil_image.size}")
        back = Background(self.pil_image.size)
        # back.set_back_gradientV(colorTop,colorBottom,0.1)
        back.set_back_gradientC(colorTop,colorBottom, 0.3)
        self.pil_image = Image.alpha_composite(back.getBackground(), self.pil_image)
        # merged_image.show()

    def setBorder(self, circle_color, circle_width=None):
        # Crea un objeto ImageDraw para dibujar en la imagen
        draw = ImageDraw.Draw(self.pil_image)
        # Obtiene las dimensiones de la self.pil_image
        width, height = self.pil_image.size
        rmax = min(width, height) // 2
        
        # Calcula el radio de la circunferencia como la mitad de la dimensión más pequeña
        if self.Cborder:
            radio =self.Cborder
        else:
            radio = rmax
            
        if circle_width is None:
            circle_width= int((rmax-radio)//2)
            radio =rmax - circle_width
              
        # Calcula el centro de la circunferencia
        centro = (width // 2, height // 2)
        # Dibuja la circunferencia
        draw.ellipse((centro[0] - radio,
                      centro[1] - radio, 
                      centro[0] + radio, 
                      centro[1] + radio),
                      outline=circle_color.value, 
                      width=circle_width)