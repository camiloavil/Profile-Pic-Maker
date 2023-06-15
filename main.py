from app.removeBack.removeCloud import removeBG_one_pic
from app.models.colors import Color, Colors
from app.models.pictures import BigPic

import os
import time
import typer
from typing_extensions import Annotated

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
def dir(dir: str, 
        colora: Annotated[str, typer.Option(help="Fisrt Color to use in the background, Default = White")] = "white",  # noqa: E501
        colorb: Annotated[str, typer.Option(help="Last Color to use in the background, Default = Black")] = "black",  # noqa: E501
        colorborder: Annotated[str, typer.Option(help="Color to use for the border, Default = White")] = None,  # noqa: E501
        osize: Annotated[bool, typer.Option(help="Origianl Size, Default = False")] = False,  # noqa: E501
        y: Annotated[bool, typer.Option(help="Force Yes, Default = False")] = False):
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
        Acolor = Color.get_color_rgb(colora)
        Bcolor = Color.get_color_rgb(colorb)
        BorderColor = None if colorborder is None else Color.get_color_rgb(colorborder)
        print(f'Checking {dir} ..., forcedYes = {y}')
        print(f"Checking Colors A:'{str(Acolor)}', B:'{str(Bcolor)}' Border:'{str(BorderColor)}'")
        print(f"Checking Original Size: {str(osize)}")
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
                        if osize is False:
                            face.resize(500)
                        face.removeBG()
                        face.addBG(Acolor,Bcolor)
                        # face.addBGPalette(Colors.BLUE_BLACK_CLEAN)
                        face.set_contour()
                        if BorderColor is not None:
                            face.setBorder(BorderColor)
                        # face.setBorder(Color.WHITE)
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
def file(file: str,
         colora: Annotated[str, typer.Option(help="Fisrt Color to use in the background, Default = White")] = "white",  # noqa: E501
         colorb: Annotated[str, typer.Option(help="Last Color to use in the background, Default = Black")] = "black",  # noqa: E501
         colorborder: Annotated[str, typer.Option(help="Color to use for the border, Default = None")] = None,  # noqa: E501
         osize: Annotated[bool, typer.Option(help="Origianl Size, Default = False")] = False,  # noqa: E501
         y: Annotated[bool, typer.Option(help="Force Yes, Default = False")] = False
         ):
    """
    Runs facial recognition on an image given its file path.
    the apply a colorfull background to it 
    :param file: A string representing the file path of the image to process.
    :return: None
    """
    Acolor = Color.get_color_rgb(colora)
    Bcolor = Color.get_color_rgb(colorb)
    BorderColor = None if colorborder is None else Color.get_color_rgb(colorborder)
    print(f"Checking '{file}' image")
    print(f"Checking Colors A:'{str(Acolor)}', B:'{str(Bcolor)}' Border:'{str(BorderColor)}'")
    print(f"Checking Original Size: {str(osize)}")
    pic_faces = BigPic(file,verbose=True).get_faces()   #get a list of FacePic objects
    for face in pic_faces:
        if osize is False:
            face.resize(500)
        face.removeBG()
        face.addBG(Acolor,Bcolor)
        # face.addBGPalette(Colors.ORANGE_BLACK_CLEAN)
        # face.addBGPalette(Colors.WHITE_TO_BROWNDARK_CLEAN)
        face.set_contour()
        if BorderColor is not None:
            face.setBorder(BorderColor)
        face.setBlur(30)
        face.show()
        if y is False:
            promp = input('Do you want to save it ? ')
        else:
            promp = 'y'
        if promp == 'y' or promp == 'yes' or promp == 'si':
            print(f"All rigth let's save it {face.get_path()}")
            face.save()

@app.command()
def showColors():
    """Show all colors available"""
    Color.print_all_names()

if __name__ == '__main__':
    app()
