from app.removeBack.removeCloud import removeBG_one_pic
from app.merging.merging import generate_gradient, merge_images
import os, time

from PIL import Image


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
        face.show()

@app.command()
def test():
    print(f'Testing ....')
    pic = Image.open('img/transparencies/IMG_20230424_120420_TIMEBURST8_out1_faces.png').convert("RGBA")
    print(f'Pic size {pic.size}')
    # pic.show()
    color_white = (255,255, 255)       # blanco
    color_black = (0.0,0)       # Negro
    color_blue = (135, 206, 250)   # Azul claro
    # color_start = (135, 206, 250)   # Azul claro
    back = generate_gradient(500, color_blue, color_white)
    merge_images(pic, back)



if __name__ == '__main__':
    app()
    # numberPath = sys.argv[1]
    # scaning_dir(f'img/input/', testing=False)
    # scaning_dir_execute(f'img/')

    # /home/camilo/software/MyPy/projectPhoto/img/IMG_20230424_073036_out1_faces.jpg
    # removeBG_one_pic('/home/camilo/software/MyPy/projectPhoto/img/IMG_20230509_155246_out2_faces.jpg')

