# APP
from ..detection.facedetetion import DetectingFaces_OP
from .background import Background
# from ..results.show import showPic
# Python
from pydantic.color import Color
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove
import logging
import threading
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
    
    def save(self,path: Optional[str]=None, tol: Optional[int] = None):
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
        if tol is not None:
            t = threading.Timer(tol, self.delete_file)
            t.start()
            logging.info('[Picture] set TimeOfLife {} seconds to delete the file pic'.format(tol))
    
    def delete_file(self):
        """
        Deletes the picture file associated with the object.

        This function checks if the `_path` attribute is not None. If it is not None, it attempts to delete the file at the specified path using the `os.remove()` function. If the file deletion is successful, it logs a message using the `logging.info()` function. If an exception occurs during the file deletion, an error message is logged using the `logging.error()` function.

        Parameters:
        - None

        Returns:
        - None
        """
        if self._path is not None:
            try:
                os.remove(self._path)
                logging.info(f'[Picture] pic deleted from path: {self._path}')
            except Exception as e:
                logging.error(f'[Picture] error deleting pic from path: {self._path}. {str(e)}')
        self._path = None

    def show(self,time: int=0,text: Optional[str]=None):
        """
        Displays an image in a window for a specified amount of time.

        Args:
            time (int, optional): The duration in seconds to display the image. Defaults to 0.
            text (str, optional): Additional text to display with the image. Defaults to None.

        Returns:
            None
        """
        logging.info('[Picture] Close the window to continue')
        # showPic(self.pil_image.copy(),time=time)
        # This line doesn't work for a api funtion
    def resize(self, width: int, height: Optional[int]=None):
        """
        Resize the picture to the given width and height.
        """
        if height is None:
            o_width, o_height = self.pil_image.size
            height = int(width * o_height // o_width)
            logging.info(f'[Picture] Resize {width} x {height}')

        self.pil_image = self.pil_image.resize((width, height))

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

    def addBG(self, colorsModel: Tuple[Color]):
        logging.info(f"[FacePic]addBG Let's add some background Center: {str(colorsModel[0])} Outer: {str(colorsModel[1])} size: {self.pil_image.size}")
        back = Background(self.pil_image.size)
        back.set_back_gradientC(colorsModel, 0.3)
        try:
            self.pil_image = Image.alpha_composite(back.getBackground(), self.pil_image)
        except Exception as e:
            logging.error(f"[FacePic]addBG Error setting the background. {e}")

    def setBorder(self, circle_color : Color, circle_width=None):
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
                      outline=circle_color.as_rgb_tuple(), 
                      width=circle_width)