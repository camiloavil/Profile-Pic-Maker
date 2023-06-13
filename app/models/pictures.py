from app.detection.facedetetion import DetectingFaces_OP
from app.models.background import Background
from app.models.colors import Color, Colors

from typing import Optional
import tkinter as tk
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from rembg import remove
import logging
import os

class Picture(): 
    _verbose = False
    def __init__(self,path: Optional[str]=None, verbose = False) -> None:
        Picture._verbose=verbose
        logging.basicConfig(level=logging.INFO)
        if os.path.isfile(path) and (path.lower().endswith('.jpg') or path.lower().endswith('.png')):
            logging.info(f'[Picture] init {path}')
            self._path=path
        else:
            logging.error(f'[Picture] Sorry "{path}" is not an Image file (jpg or png)')
            self._path=None

    def get_path(self):
        return self._path
    
    def save(self,path: Optional[str]=None):
        """
        Save the picture to the given path. If no path is given and a path is already set, 
        save the picture to the existing path. If no path is given and no path is set, 
        do nothing. The path parameter is optional. 
        
        :param path: (Optional) The path to save the picture to.
        :type path: str
        
        :return: None
        :rtype: NoneType
        """
        if path is not None:
            if os.path.exists(path) is False:
                self._path=path
                self.pil_image.save(self._path)
            else:
                logging.info('[Picture] let\'s save the pic on this path {}'.format(self._path))
        
        if self._path is not None:
            if os.path.exists(self._path):
                logging.error(f'[Picture] this path {self._path} already exists')
                return
        self.pil_image.save(self._path)
        logging.info('[Picture] pic saved on this path {}'.format(self._path))

    def show(self,text: Optional[str]=None):
        """
        Shows or closes the PIL image based on the value of the 'show' parameter.
        this will do whit the default view of the PIL image

        :param show: A boolean indicating whether to show or close the PIL image.
        :type show: bool
        """
        logging.info('[Picture] Close the window to continue')
        window = tk.Tk()
        window.title('Close the window to continue')
        # Copy the Imagen of PIL object
        image_thumbnail = self.pil_image.copy()
        # make a thumbnail of the image
        image_thumbnail.thumbnail((250, 250))
        # Create a PhotoImage object from the image
        photo = ImageTk.PhotoImage(image_thumbnail)
        # Create a label to display the image
        label = tk.Label(image=photo)
        label.pack()
        # Start the GUI event loop
        window.mainloop()

class BigPic(Picture):
    def get_faces(self):    #Metodo to indentify and get Faces of the big Pic
        if self._path is None:
            logging.error('[BigPic] Sorry there is not a pic')
            return None
        
        # Get faces as a list of PIL images
        faces = DetectingFaces_OP(file=self._path).get_PIL_faces()   
        logging.info(f'[BigPic] {len(faces)} faces detected')
        optional_path = None
        if self._path.endswith('.jpg'):
            optional_path = self._path.replace('.jpg','[FACE]_')
        elif self._path.endswith('.png'):
            optional_path = self._path.replace('.png','[FACE]_')
        #convert to isntancias of FacePic model        
        return [FacePic(img=face, path_Optional=optional_path+str(i)) for i,face in enumerate(faces)]

class FacePic(Picture):
    def __init__(self, 
                 path: Optional[str]=None, 
                 img=None, 
                 path_Optional: Optional[str]=None) -> None:
        if path is not None: 
            super().__init__(path)
            logging.info(f'[FacePic]init objeto FILE FacePic path {path}')
        if img is not None:
            self.pil_image=img
            if path_Optional is not None:
                self._path=path_Optional+'.png'
                logging.info(f'[FacePic]init TEMPORAL objet FacePic path {self._path}')
            else:
                self._path=None
                logging.info('[FacePic]init TEMPORAL objet FacePic whitout path')
        else:
            logging.error('[FacePic]init empty objeto')

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
        #Máscara para el área fuera del círculo
        mask = Image.new("L", (self.pil_image.size), 0)  
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