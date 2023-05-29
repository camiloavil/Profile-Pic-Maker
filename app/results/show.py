import time, subprocess


def showPic(file:str):
        # Mostrar la imagen utilizando el programa externo
    subprocess.Popen(["eog", file])
    time.sleep(7)

    subprocess.Popen(["pkill", "eog"])

    # Eliminar el archivo temporal
    subprocess.Popen(["rm", file])