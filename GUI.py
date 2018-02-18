import tkinter as tk
import os

from PIL import ImageTk, Image
from time import sleep
from capture import takeCapture
from faceDetection import faceDetect
from camera_cv import mainFunction
    

class MainApplication(tk.Frame):  
    def __init__(self, parent, *args, **kwargs):
        def callback():
            path = takeCapture()
            img = ImageTk.PhotoImage(Image.open(path))
            data = faceDetect(path)
            image.configure(image=img)
            image.image = img

            smileInput.configure(text = data[0])
            genderInput.configure(text = data[1])
            ageInput.configure(text = data[2])
            glassesInput.configure(text = data[3])
            hairInput.configure(text = data[4])
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.state('zoomed')
        parent.title("Face recognition software")
        imageFrame = tk.Frame(parent)
        buttons = tk.Frame(parent)
        imageFrame.pack(side = tk.TOP)
        buttons.pack()
        img = ImageTk.PhotoImage(Image.open("picture.jpg"))
        image = tk.Label(imageFrame, image=img)
        image.pack(fill = "both", expand = "yes")
        

        pictureButton = tk.Button(buttons, text="Take picture", command=callback)
        detectObjectsButton = tk.Button(buttons, text="Detect objects", command=mainFunction)
        quitButton = tk.Button(buttons, text="Quit", command=quit)

        genderLabel = tk.Label(buttons, text = "Gender: ")
        ageLabel = tk.Label(buttons, text = "Age: ")
        smileLabel = tk.Label(buttons, text = "Smile: ")
        hairLabel = tk.Label(buttons, text = "Facial Hair: ")
        glassesLabel = tk.Label(buttons, text = "Glasses: ")

        genderInput = tk.Label(buttons, text = "")
        ageInput = tk.Label(buttons, text = "")
        smileInput = tk.Label(buttons, text = "")
        hairInput = tk.Label(buttons, text = "")
        glassesInput = tk.Label(buttons, text = "")

        genderLabel.pack()
        genderInput.pack()
        ageLabel.pack()
        ageInput.pack()
        smileLabel.pack()
        smileInput.pack()
        hairLabel.pack()
        hairInput.pack()
        glassesLabel.pack()
        glassesInput.pack()
        pictureButton.pack()
        detectObjectsButton.pack()
        quitButton.pack()
        
        callback()

    


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()



