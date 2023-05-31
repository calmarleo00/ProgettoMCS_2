# Import required libraries
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

file_path = "bridge.bmp"
global label_left, label_right, image, resized_image


def resize_image(image, container_width, container_height) :
    global resized_image
    img_width = int(image.width)
    img_height = int(image.height)
    resized_image = image
    #if img_width > container_width or img_height > container_height :
    if img_width > img_height :
        wpercent = (container_width/float(img_width))
        hsize = int((float(img_height)*float(wpercent)))
        resized_image = image.resize((container_width,hsize), Image.Resampling.LANCZOS)
    elif img_width <= img_height :
        hpercent = (container_height/float(img_height))
        wsize = int((float(img_width)*float(hpercent)))
        resized_image = image.resize((wsize,container_height), Image.Resampling.LANCZOS)
    return resized_image

def change_image() :
    global label_left, label_right
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    container_width = 200
    container_height = 200
    resized_image = resize_image(image, container_width, container_height)
    original_image = ImageTk.PhotoImage(resized_image)
    label_left.configure(image=original_image)
    label_left.image = original_image

    container_width = 650
    container_height = 400
    main_image_resized = resize_image(image, container_width, container_height)
    main_image = ImageTk.PhotoImage(main_image_resized)
    label_right.configure(image=main_image)
    label_right.image = main_image
def main_loop():
    global image, resized_image, label_left, label_right
    root = Tk()  # create root window
    root.title("Basic GUI Layout")  # title of the GUI window
    root.maxsize(1024, 756)  # specify the max size the window can expand to
    root.config(bg="skyblue")  # specify background color

    # Create left and right frames
    left_frame = Frame(root, width=200, height=400, bg='grey')
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    right_frame = Frame(root, width=650, height=400, bg='grey')
    right_frame.grid(row=0, column=1, padx=10, pady=5)

    # Create frames and labels in left_frame
    Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

    # load image to be "edited"
    image = Image.open(file_path)
    #label = tkinter.Label(left_frame, image=ImageTk.PhotoImage(image))

    #resize image
    container_width = 200
    container_height = 200
    resized_image = resize_image(image, container_width, container_height)
    
    original_image = ImageTk.PhotoImage(resized_image)#.subsample(3,3)  # resize image using subsample
    label_left = Label(left_frame, image=original_image)
    label_left.grid(row=1, column=0, padx=5, pady=5)
    #resize image
    container_width = 650
    container_height = 400
    main_image_resized = resize_image(image, container_width, container_height)
    main_image = ImageTk.PhotoImage(main_image_resized)
    label_right = Label(right_frame, image=main_image)
    label_right.grid(row=0,column=0, padx=5, pady=5)
    # Display image in right_frame

    # Create tool bar frame
    tool_bar = Frame(left_frame, width=180, height=185)
    tool_bar.grid(row=2, column=0, padx=5, pady=5)

    # Example labels that serve as placeholders for other widgets
    Button(tool_bar, text="Dialog", command=change_image).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
    Label(tool_bar, text="Filters", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)
    root.mainloop()


if __name__ == '__main__' :
    main_loop()