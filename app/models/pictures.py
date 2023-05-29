from app.detection.facedetetion import DetectingFaces_OP
import os

class Picture(): 
    _debug = False
    def __init__(self,url: str, debug = False) -> None:
        Picture._debug=debug
        if os.path.isfile(url) and (url.lower().endswith('.jpg') or url.lower().endswith('.png')):
            if Picture._debug: print(f'[INFO_Picture] init {url} picture')
            self._url=url
        else:
            if Picture._debug: print(f'[ERROR_Picture] Sorry "{url}" is not an Image file (jpg or png)')
            self._url=None

    def get_url(self):
        return self._url

class Bigpic(Picture):
    def get_faces(self):
        if self._url is None:
            if Picture._debug: print(f'[ERROR_Bigpic] Sorry there is not a pic')
            return None
        else:
            if Picture._debug: print(f'[INFO_Bigpic] process to detect Faces expected List of faces')
            DetectingFaces_OP(file=self._url)
            return None
