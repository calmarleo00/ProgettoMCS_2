from tkinter import *
from PIL import Image, ImageTk

def resize_image(image, container_width, container_height) :
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

root = Tk()  # create root window
root.title("Basic GUI Layout")  # title of the GUI window
root.maxsize(1080, 720)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color

# Create left and right frames
left_frame = Frame(root, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(root, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

# Create frames and labels in left_frame
Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

# load image to be "edited"
image = Image.open("20x20.bmp")
original_image = resize_image(image, 200, 200)  # resize image using subsample
Label(left_frame, image=ImageTk.PhotoImage(original_image)).grid(row=1, column=0, padx=5, pady=5)

# Display image in right_frame
Label(right_frame, image=ImageTk.PhotoImage(image)).grid(row=0,column=0, padx=5, pady=5)

# Create tool bar frame
tool_bar = Frame(left_frame, width=180, height=185)
tool_bar.grid(row=2, column=0, padx=5, pady=5)

# Example labels that serve as placeholders for other widgets
Label(tool_bar, text="Tools", relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
Label(tool_bar, text="Filters", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

# Example labels that could be displayed under the "Tool" menu
Label(tool_bar, text="Select").grid(row=1, column=0, padx=5, pady=5)
Label(tool_bar, text="Crop").grid(row=2, column=0, padx=5, pady=5)
Label(tool_bar, text="Rotate & Flip").grid(row=3, column=0, padx=5, pady=5)
Label(tool_bar, text="Resize").grid(row=4, column=0, padx=5, pady=5)
Label(tool_bar, text="Exposure").grid(row=5, column=0, padx=5, pady=5)
root.mainloop()


