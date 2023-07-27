from typing import Tuple
from PIL import Image, ImageDraw
from pydantic.color import Color
import random

class Background():
    def __init__(self,pix_w: int, pix_h: int) -> None:
        self._pix_w=pix_h
        self._pix_h=pix_h
        self._background = Image.new("RGBA", (pix_w, pix_h), (0, 0, 0, 0))

    def __init__(self,size: tuple) -> None:
        self._pix_w=size[0]
        self._pix_h=size[1]
        self._background = Image.new("RGBA", size, (0, 0, 0, 0))
    
    @staticmethod
    def interpolate_color(color_start, color_end, t):
        # Interpolar los componentes RGB entre los dos colores basado en el valor t
        r = int((1 - t) * color_start[0] + t * color_end[0])
        g = int((1 - t) * color_start[1] + t * color_end[1])
        b = int((1 - t) * color_start[2] + t * color_end[2])
        return (r, g, b)    
    
    def set_back_gradientH(self,
                           colorTop: Color,
                           colorBottom: Color, 
                           pColorcircle: float):
        colorTop_ = colorTop.value
        colorBottom_ = colorBottom.value
        draw = ImageDraw.Draw(self._background)
        long_range = self._pix_w
        start_index = int(long_range * pColorcircle)
        for i in range(long_range):
            if i < start_index:
                draw.line([(i, 0), (i, self._pix_h - 1)], fill=colorTop_)
            else:
                t = (i - start_index) / (long_range - start_index)
                color = Background.interpolate_color(colorTop_, colorBottom_, t)
                draw.line([(i, 0), (i, self._pix_h - 1)], fill=color)
    
    def set_back_gradientV(self, 
                           colorLeft: Color, 
                           colorRight: Color, 
                           pColorcircle: float):
        colorLeft_ = colorLeft.value
        colorRight_ = colorRight.value
        draw = ImageDraw.Draw(self._background)
        long_range = self._pix_h
        start_index = int(long_range * pColorcircle)
        for i in range(long_range):
            if i < start_index:
                draw.line([(0, i), (self._pix_w - 1, i)], fill=colorLeft_)
            else:
                t = (i - start_index) / (long_range - start_index)
                color = Background.interpolate_color(colorLeft_, colorRight_, t)
                draw.line([(0, i), (self._pix_w - 1, i)], fill=color)

    def set_back_gradientC(self,
                           colorModel: Tuple[Color], 
                           pColorcircle: float):
        try:
            colorCenter_ = colorModel[0].as_rgb_tuple()
            colorOuter_ = colorModel[1].as_rgb_tuple()
        except Exception as e:
            print(f"[Background]set_back_gradientC Error setting Colors of background. {e}")
            return
        draw = ImageDraw.Draw(self._background)
        center_x = self._pix_w // 2
        center_y = self._pix_h // 2
        #se Definen radios de rango - Define radius of range
        r_max = int(min(center_x, center_y))
        r_IBorder = int(r_max * pColorcircle)
        for y in range(self._pix_h):
            for x in range(self._pix_w):
                pxl_radius = int(((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5)
                if pxl_radius < r_IBorder: #First ring of the circle
                    draw.point((x, y), fill=colorCenter_)
                elif pxl_radius <= r_max: #Second ring of the circle
                    t = (pxl_radius - r_IBorder) / (r_max - r_IBorder)
                    color = self.interpolate_color(colorCenter_, colorOuter_, t)
                    draw.point((x, y), fill=color)

    def set_back_gradientC_old(self,
                           colorCenter: Color, 
                           colorOuter: Color, 
                           pColorcircle: float, 
                           p_radius: float):
        colorCenter_ = colorCenter.value
        colorOuter_ = colorOuter.value
        draw = ImageDraw.Draw(self._background)
        center_x = self._pix_w // 2
        center_y = self._pix_h // 2
        #se Definen radios de rango - Define radius of range
        r_max = min(center_x, center_y)
        r_IIBorder = int(r_max * p_radius)
        r_IBorder = int(r_max * pColorcircle)
        for y in range(self._pix_h):
            for x in range(self._pix_w):
                pxl_radius = int(((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5)
                if pxl_radius < r_IBorder: #First ring of the circle
                    draw.point((x, y), fill=colorCenter_)
                elif pxl_radius <= r_IIBorder: #Second ring of the circle
                    t = (pxl_radius - r_IBorder) / (r_max - r_IBorder)
                    color = self.interpolate_color(colorCenter_, colorOuter_, t)
                    draw.point((x, y), fill=color)
                # elif pxl_radius < r_max:
                #     #last ring of the circle this is a Try for a fade efect
                #     t = 1 - (pxl_radius - r_IIBorder) / (r_max - r_IIBorder) * 0.9
                #     if random.random() <= t:
                #         draw.point((x, y), fill=(colorOuter_[0],colorOuter_[1],colorOuter_[2],int(t*200)))
                #         # print(f'Center{int(t*255)} - {colorOuter_} - {(colorOuter_[0],colorOuter_[1],colorOuter_[2],int(t*255))}')

    def set_back_gradientCefect(self, colorCenter: Color, colorOuter: Color, pColorcircle: float, p_radius: float):
        colorCenter_ = colorCenter.value
        colorOuter_ = colorOuter.value
        draw = ImageDraw.Draw(self._background)
        center_x = self._pix_w // 2
        center_y = self._pix_h // 2
        max_radius = max(center_x, center_y) * p_radius
        start_distance = max_radius * pColorcircle
        for y in range(self._pix_h):
            for x in range(self._pix_w):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if distance < start_distance:
                    #Distance inside of pColorcircle p is for percentage
                    draw.point((x, y), fill=colorCenter_)
                elif distance <= max_radius:
                    if random.random() <= 0.7:
                        t = (distance - start_distance) / (max_radius - start_distance)
                        color = self.interpolate_color(colorCenter_, colorOuter_, t)
                        draw.point((x, y), fill=color)

    def getBackground(self):
        return self._background
    
    def show(self):
        self._background.show()
