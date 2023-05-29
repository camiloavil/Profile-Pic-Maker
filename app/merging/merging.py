from PIL import Image, ImageDraw
from app.results.show import showPic

def generate_gradient(diameter, color_start, color_end):
    # Crear una nueva imagen RGBA con fondo transparente
    l_x = 500
    l_y = 500
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

    showPic(temp_image_path)