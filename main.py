from app.detection.facedetetion import scaning_dir
from app.removeBack.removebg import removeBG_one_pic
import os, time

from PIL import Image, ImageDraw

def generate_circle_gradient(diameter):
    # Crear una nueva imagen RGBA con fondo transparente
    image = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Coordenadas del centro del círculo
    center_x = diameter // 2
    center_y = diameter // 2

    # Generar un gradiente radial de color
    for y in range(diameter):
        for x in range(diameter):
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            normalized_distance = distance / (diameter // 2)
            color_value = int(normalized_distance * 255)
            draw.point((x, y), (color_value, color_value, color_value))

    # Mostrar la imagen generada
    image.show()

def scaning_dir_execute(dir):        #iterate into a directory looking for every jpg file
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            if(file.endswith(".jpg")):
                print(f"let's check this image -> {os.path.join(subdir, file)}")
                removeBG_one_pic(os.path.join(subdir, file))
                time.sleep(15)      #to no overprocess the API and get error
                # ImageProcess(os.path.join(subdir, file), )


if __name__ == '__main__':
    # numberPath = sys.argv[1]
    # scaning_dir(f'img/input/', testing=False)
    scaning_dir_execute(f'img/')

    # /home/camilo/software/MyPy/projectPhoto/img/IMG_20230424_073036_out1_faces.jpg
    # removeBG_one_pic('/home/camilo/software/MyPy/projectPhoto/img/IMG_20230509_155246_out2_faces.jpg')