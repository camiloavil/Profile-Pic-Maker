import tkinter as tk
from PIL import Image, ImageTk


def showPic(pil_image: Image, time: int=0):
        """
        Display an image in a Tkinter window.

        Args:
            pil_image (Image): The PIL image object to be displayed.
            time (int, optional): The time in seconds for which the window should be displayed. Default is 0.

        Returns:
            None
        """
        window = tk.Tk()
        window.title('Close the window to continue')
        # Copy the Imagen of PIL object
        image_thumbnail = pil_image.copy()
        # make a thumbnail of the image
        image_thumbnail.thumbnail((250, 250))
        # Create a PhotoImage object from the image
        photo = ImageTk.PhotoImage(image_thumbnail)
        # Create a label to display the image
        label = tk.Label(image=photo)
        label.pack()
        
        if time > 0:
            window.after(time*1000, window.destroy)
        # Start the GUI event loop
        window.mainloop()
    