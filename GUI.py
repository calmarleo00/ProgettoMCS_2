from scipy.fftpack import dct, idct
from tkinter import *
from tkinter import filedialog, ttk
import numpy as np
from PIL import ImageTk, Image
from ttkthemes import ThemedTk

global file_path, left_image_container, right_image_container, resized_image, image_array, left_image_size, \
right_image_size, image


class ImageManager:
    def dct2(self, matrix):
        return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

    def idct2(self, matrix):
        return idct(idct(matrix.T, norm='ortho').T, norm='ortho')

    def resize_image(self, image, container_width, container_height):
        global resized_image
        img_width = int(image.width)
        img_height = int(image.height)
        resized_image = image
        # if img_width > container_width or img_height > container_height :
        if img_width > img_height:
            wpercent = (container_width / float(img_width))
            hsize = int((float(img_height) * float(wpercent)))
            resized_image = image.resize((container_width, hsize), Image.Resampling.LANCZOS)
        elif img_width <= img_height:
            hpercent = (container_height / float(img_height))
            wsize = int((float(img_width) * float(hpercent)))
            resized_image = image.resize((wsize, container_height), Image.Resampling.LANCZOS)
        return resized_image

    def set_image(self, image, container):
        tk_image = ImageTk.PhotoImage(image)
        container.configure(image=tk_image)
        container.image = tk_image

    def change_image(self, f_scaling, left_image_container, right_image_container):
        global left_image_size, right_image_size, image_array, resized_image, file_path, image
        file_path = filedialog.askopenfilename()
        image = Image.open(file_path).convert('L')

        image_array = np.asarray(image)

        resized_image = self.resize_image(image, left_image_size, left_image_size)
        self.set_image(resized_image, left_image_container)

        main_image_resized = self.resize_image(image, right_image_size, right_image_size)
        self.set_image(main_image_resized, right_image_container)

        if image.width > image.height:
            max_scale_f = image.height
        else:
            max_scale_f = image.width

        f_scaling.configure(to=max_scale_f)
        f_scaling.to = max_scale_f

    def set_max_scale_d(self, *args):
        global max_scale_d
        max_scale_d = (2 * args[4].get()) - 2
        args[3].configure(to=max_scale_d)
        args[3].to = max_scale_d
        if float(args[5].get()) > max_scale_d:
            args[5].set(max_scale_d)

    def accept_whole_number_only(self, *args):
        scaling = args[len(args) - 1].get()
        if int(scaling) != scaling:
            args[len(args) - 1].set(int(scaling))

    def compress(self, image_array, right_image_container, f_scaling, d_scaling):
        global right_image_size
        if f_scaling != 1:
            f_scaling = int(f_scaling)
            d_scaling = int(d_scaling)
            extra_row = 0
            extra_col = 0
            if image_array.shape[0] % f_scaling != 0:
                extra_row = image_array.shape[0] % f_scaling
            if image_array.shape[1] % f_scaling != 0:
                extra_col = image_array.shape[1] % f_scaling

            array_split = self.split(image_array, f_scaling)
            for i in range(len(array_split)):
                array_split[i] = self.dct2(array_split[i])
                for row in range(array_split[i].shape[0]):
                    for col in range(array_split[i].shape[1]):
                        if row + col >= d_scaling:
                            array_split[i][row, col] = 0
                array_split[i] = self.idct2(array_split[i])

            n_blocks_rows = int(image_array.shape[0] / f_scaling)
            n_blocks_cols = int(image_array.shape[1] / f_scaling)
            i = 0
            image_result = np.ndarray(shape=(image_array.shape[0] - extra_row, image_array.shape[1] - extra_col),
                                      dtype=int)
            for x in range(n_blocks_rows):
                for y in range(n_blocks_cols):
                    image_result[(x * f_scaling):(x * f_scaling + f_scaling),
                    (y * f_scaling):(y * f_scaling + f_scaling)] = array_split[i]
                    i += 1
            image_result[image_result < 0] = 0
            image_result[image_result > 255] = 255

            # for i in range (image_result.shape[0] - extra_row, image_result.shape[0]):
            #    image_result[i,:] = image_result[image_result.shape[0] - extra_row - 1, :]

            # for i in range (image_result.shape[1] - extra_col, image_result.shape[1]):
            #    image_result[:,i] = image_result[:,image_result.shape[1] - extra_col - 1]

            image = Image.fromarray(image_result)
            main_image_resized = self.resize_image(image, right_image_size, right_image_size)
            main_image = ImageTk.PhotoImage(main_image_resized)
            right_image_container.configure(image=main_image)
            right_image_container.image = main_image

    def split(self, matrix, scaling):
        f_scaling = int(scaling)
        extra_row = 0
        extra_col = 0
        if matrix.shape[0] % f_scaling != 0:
            extra_row = matrix.shape[0] % f_scaling
        if matrix.shape[1] % f_scaling != 0:
            extra_col = matrix.shape[1] % f_scaling
        array_split = []
        matrix_slice = matrix[0:(matrix.shape[0] - extra_row), 0:(matrix.shape[1] - extra_col)]
        n_blocks_rows = int(matrix_slice.shape[0] / f_scaling)
        n_blocks_cols = int(matrix_slice.shape[1] / f_scaling)

        for x in range(n_blocks_rows):
            for y in range(n_blocks_cols):
                tmp = matrix_slice[(x * f_scaling):(x * f_scaling + f_scaling),
                      (y * f_scaling):(y * f_scaling + f_scaling)]
                array_split.append(tmp)
        return array_split


class GUI:
    def main_loop(self):
        global image, resized_image, image_array, left_image_size, right_image_size, max_scale_d, file_path, d_scaling
        filepath = ""
        left_image_size = 400
        right_image_size = 600
        max_scale_d = 0

        imageManager = ImageManager()
        # CREATE WINDOW
        root = ThemedTk(theme='black')
        root.title("Compressione di immagini")
        root.state("zoomed")  # Permette alla finestra di partire a schermo intero
        # style = ttkthemes.ThemedStyle(root)
        # style.theme_use('yaru')
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.minsize(screen_width, screen_height)  # Impostiamo la grandezza minima

        root.config(bg="#000000")  # specify background color

        root.columnconfigure(0, weight=1)  # impostazione griglia
        root.columnconfigure(1, weight=3)

        root.rowconfigure(0, weight=3)
        # Create left and right frames
        left_frame = Frame(root, bg='#333333')
        left_frame.grid(row=0, column=0, sticky="nsew", pady=20)
        right_frame = Frame(root, bg='#333333')
        right_frame.grid(row=0, column=1, sticky="nsew", pady=20)

        left_frame.columnconfigure(0, weight=0)
        left_frame.columnconfigure(1, weight=0)
        left_frame.columnconfigure(2, weight=0)
        left_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        left_frame.rowconfigure(2, weight=1)
        left_frame.rowconfigure(3, weight=1)
        left_frame.rowconfigure(4, weight=1)
        left_frame.rowconfigure(5, weight=1)

        right_frame.rowconfigure(0, weight=3)
        right_frame.columnconfigure(0, weight=3)
        # Create frames and labels in left_frame
        original_name = ttk.Label(left_frame, text="Immagine originale")
        original_name.grid(row=0, column=0, columnspan=3)

        image = Image.open('C:/Users/delfi/PycharmProjects/Progetto_MCS2/deer.bmp').convert('L')
        #image = Image.new("L", (512, 512), "black")

        if image.width > image.height:
            max_scale_f = image.height
        else:
            max_scale_f = image.width

        image_array = np.asarray(image)
        #image_array = []

        original_image = ImageTk.PhotoImage(imageManager.resize_image(image, left_image_size, left_image_size))
        left_image_container = ttk.Label(left_frame, image=original_image)
        left_image_container.grid(row=1, column=0, columnspan=3)
        left_image_container.image = original_image

        # resize image
        main_image = ImageTk.PhotoImage(imageManager.resize_image(image, right_image_size, right_image_size))
        right_image_container = ttk.Label(right_frame, image=main_image)
        right_image_container.grid(row=0, column=0)
        right_image_container.image = main_image

        ttk.Button(left_frame, text="Seleziona immagine", command=lambda:
        imageManager.change_image(f_scaling, left_image_container, right_image_container)
                   ).grid(row=2, column=0, sticky="n", columnspan=3)

        ttk.Label(left_frame, text="F: ").grid(row=3, column=0)

        f_value = IntVar(value=1)
        f_scaling = ttk.Scale(left_frame, from_=1, to=max_scale_f, orient=HORIZONTAL, length=left_image_size,
                              variable=f_value)
        f_scaling.grid(row=3, column=1)

        ttk.Entry(left_frame, textvariable=f_value, width=7).grid(row=3, column=2)

        ttk.Label(left_frame, text="d: ").grid(row=4, column=0)

        d_value = IntVar(value=0)
        d_scaling = ttk.Scale(left_frame, from_=0, to=max_scale_d, orient=HORIZONTAL, length=left_image_size,
                              variable=d_value)
        d_scaling.grid(row=4, column=1)
        ttk.Entry(left_frame, textvariable=d_value, width=7).grid(row=4, column=2)

        f_value.trace(mode="w", callback=lambda *args, ds=d_scaling, f_value=f_value, d_value=d_value: [
            imageManager.set_max_scale_d(*args, ds, f_value, d_value),
            imageManager.accept_whole_number_only(f_scaling)])
        d_value.trace(mode="w", callback=lambda *args, ds=d_scaling: imageManager.accept_whole_number_only(*args, ds))
        ttk.Button(left_frame, text="Comprimi",
                   command=lambda: imageManager.compress(image_array, right_image_container, f_scaling.get(),
                                                         d_scaling.get())
                   ).grid(row=5, column=0, columnspan=3, sticky="n")
        root.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.main_loop()
