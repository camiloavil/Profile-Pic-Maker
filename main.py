from app.detection.facedetetion import scaning_dir
from app.removeBack.removebg import removeBG_one_pic
import os, time, subprocess

from PIL import Image, ImageDraw

def generate_circle_gradient(diameter, color_start, color_end):
    # Crear una nueva imagen RGBA con fondo transparente
    image = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Coordenadas del centro del círculo
    center_x = diameter // 2
    center_y = diameter // 2

    # Generar un gradiente longitudinal de color
    for y in range(diameter):
        t = y / diameter
        color = interpolate_color(color_start, color_end, t)
        draw.line([(0, y), (diameter-1, y)], fill=color)

    return image
    # Mostrar la imagen generada
    image.show()

def interpolate_color(color_start, color_end, t):
    # Interpolar los componentes RGB entre los dos colores basado en el valor t
    r = int((1 - t) * color_start[0] + t * color_end[0])
    g = int((1 - t) * color_start[1] + t * color_end[1])
    b = int((1 - t) * color_start[2] + t * color_end[2])
    return (r, g, b)

def merge_images(pic: Image, background: Image):
    # background = Image.open(background_image_path).convert("RGBA")

    # Redimensionar la imagen generada para que coincida con el tamaño de la imagen de fondo
    # overlay_resized = overlay_image.resize(background.size)
    merged_image = Image.alpha_composite(background, pic)

    # merged_image.show()
    temp_image_path = "/tmp/temp_merged_image.png"
    merged_image.save(temp_image_path)

    # Mostrar la imagen utilizando el programa externo
    subprocess.Popen(["eog", temp_image_path])

    # Esperar 7 segundos
    time.sleep(7)

    # Cerrar la ventana del visualizador de imágenes
    subprocess.Popen(["pkill", "eog"])

    # Eliminar el archivo temporal
    subprocess.Popen(["rm", temp_image_path])

    # time.sleep(5)
    # merged_image.close()

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
    # scaning_dir_execute(f'img/')

    # /home/camilo/software/MyPy/projectPhoto/img/IMG_20230424_073036_out1_faces.jpg
    # removeBG_one_pic('/home/camilo/software/MyPy/projectPhoto/img/IMG_20230509_155246_out2_faces.jpg')

    pic = Image.open('img/transparencies/IMG_20230424_120420_TIMEBURST8_out1_faces.png').convert("RGBA")
    print(f'Pic size {pic.size}')
    # pic.show()
    color_end = (0, 0, 0)       # Negro
    color_start = (135, 206, 250)   # Azul claro
    back = generate_circle_gradient(500, color_start, color_end)
    merge_images(pic, back)
