from scipy.fftpack import dct, idct
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np


def idct2(matrix):
    return idct(idct(matrix.T, norm='ortho').T, norm='ortho')


def dct2(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')


def change_image(left_image_container, right_image_container, left_image_size, right_image_size, max_scale_f, f_scaling,
                 image_array):
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path).convert('L')
    image_array = np.asarray(image)

    resized_image = resize_image(image, left_image_size, left_image_size)
    original_image = ImageTk.PhotoImage(resized_image)
    left_image_container.configure(image=original_image)
    left_image_container.image = original_image

    main_image_resized = resize_image(image, right_image_size, right_image_size)
    main_image = ImageTk.PhotoImage(main_image_resized)
    right_image_container.configure(image=main_image)
    right_image_container.image = main_image

    if (image.width > image.height):
        max_scale_f = image.height
    else:
        max_scale_f = image.width

    f_scaling.configure(to=max_scale_f)
    f_scaling.to = max_scale_f


def set_max_scale_d():
    global max_scale_d, d_scaling, f_scaling
    max_scale_d = (2 * f_scaling.get()) - 2
    d_scaling.configure(to=max_scale_d)
    d_scaling.to = max_scale_d


class ImageManager:

    def resize_image(image, container_width, container_height):
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

    def compress(image_array, f_scaling, d_scaling):
        global right_image_container, right_image_size
        extra_row = 0
        extra_col = 0
        if (image_array.shape[0] % f_scaling != 0):
            extra_row = image_array.shape[0] % f_scaling
        if (image_array.shape[1] % f_scaling != 0):
            extra_col = image_array.shape[1] % f_scaling

        array_split = split(image_array, f_scaling)
        for i in range(len(array_split)):
            array_split[i] = dct2(array_split[i])
            for row in range(array_split[i].shape[0]):
                for col in range(array_split[i].shape[1]):
                    if row + col >= d_scaling:
                        array_split[i][row, col] = 0
            array_split[i] = idct2(array_split[i])

        n_blocks_rows = int(image_array.shape[0] / f_scaling)
        n_blocks_cols = int(image_array.shape[1] / f_scaling)
        i = 0
        image_result = np.ndarray(shape=(image_array.shape[0] - extra_row, image_array.shape[1] - extra_col), dtype=int)
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
        main_image_resized = resize_image(image, right_image_size, right_image_size)
        main_image = ImageTk.PhotoImage(main_image_resized)
        right_image_container.configure(image=main_image)
        right_image_container.image = main_image

    def split(matrix, f_scaling):
        extra_row = 0
        extra_col = 0
        if (matrix.shape[0] % f_scaling != 0):
            extra_row = matrix.shape[0] % f_scaling
        if (matrix.shape[1] % f_scaling != 0):
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
