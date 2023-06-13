from app.removeBack.removeCloud import removeBG_one_pic
from app.models.colors import Color, Colors
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
def dir(dir: str, y: bool = False):
    """
    Runs a directory check and processes all .jpg files contained in it. 
    For each .jpg file found, it detects faces and prompts the user for further action, 
    including adding a background palette, setting contours, and setting a black border. 
    The processed image can be saved upon user request. 

    Parameters:
    dir (str): the filepath of the directory to be checked
    y (bool): if True, forces yes to all actions

    Returns:
    None
    """
    if os.path.isdir(dir):
        print(f'Checking {dir} ..., forcedYes = {y}')
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith(".jpg"):
                print(f"\tlet's check this image -> {os.path.join(dir,file)}")
                pic_faces = BigPic(os.path.join(dir,file),verbose=True).get_faces()   #get a list of FacePic objects
                print(f'\t{len(pic_faces)} faces detected')
                for face in pic_faces:
                    face.show(time=3)
                    if y is False:
                        promp = input('Do you want to continue whit this Pic ? (y/n) :')
                    else:
                        promp = 'y'
                    if promp == 'y' or promp == 'yes' or promp == 'si':
                        face.removeBG()
                        face.addBGPalette(Colors.BLUE_BLACK_CLEAN)
                        face.set_contour()
                        face.setBorder(Color.WHITE)
                        face.setBlur(30)
                        face.show(time=3)
                        if y is False:
                            promp = input('Do you want to save it ? ')
                        if promp == 'y' or promp == 'yes' or promp == 'si':
                            print(f"All rigth let's save it {face.get_path()}")
                            face.save()
    else:
        print(f'[ERROR] Sorry "{dir}" is not an active directory')

@app.command()
def file(file: str):
    """
    Runs facial recognition on an image given its file path.
    the apply a colorfull background to it 
    :param file: A string representing the file path of the image to process.
    :return: None
    """
    print(f"Cheking '{file}' image")
    pic_faces = BigPic(file,verbose=True).get_faces()   #get a list of FacePic objects
    for face in pic_faces:
        face.removeBG()
        # face.addBG(Color.BLUE_SKY,Color.BLACK)
        face.addBGPalette(Colors.ORANGE_BLACK_CLEAN)
        face.set_contour()
        face.setBorder(Color.WHITE)
        face.setBlur(30)
        face.show()
        promp = input('Do you want to save it ? ')
        if promp == 'y' or promp == 'yes' or promp == 'si':
            print(f"All rigth let's save it {face.get_path()}")
            face.save()

@app.command()
def test():
    """Testing command"""
    print('Testing ....')

if __name__ == '__main__':
    app()
