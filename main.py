from app.removeBack.removeCloud import removeBG_one_pic
from app.models.colors import Colors
import os
import time

import typer
from app.models.pictures import BigPic

app = typer.Typer()

def scaning_dir_execute(dir):        #iterate into a directory looking for every jpg file
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            if(file.endswith(".jpg")):
                print(f"let's check this image -> {os.path.join(subdir, file)}")
                removeBG_one_pic(os.path.join(subdir, file))
                time.sleep(15)      #to no overprocess the API and get error
                # ImageProcess(os.path.join(subdir, file), )

@app.command()
def dir(dir: str):
    if os.path.isdir(dir):
        print(f'Checking {dir} ...')
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith(".jpg"):
                # print(f"\tlet's check this image -> {os.path.join(subdir, file)}")
                print(f"\tlet's check this image -> {os.path.join(dir,file)}")
    else:
        print(f'[ERROR] Sorry "{dir}" is not an active directory')

@app.command()
def file(file: str):
    print(f"Cheking '{file}' image")
    pic_faces = BigPic(file,verbose=True).get_faces()   #get a list of FacePic objects
    for face in pic_faces:
        face.removeBG()
        # face.addBG(Color.BLUE_SKY,Color.BLACK)
        face.addBGPalette(Colors.WET_ASPHALT_TO_GREEN_SEA)
        face.set_contour()
        face.setBlur(30)
        face.show()

@app.command()
def test():
    print('Testing ....')

if __name__ == '__main__':
    app()
