import os

import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)


def init():
    image_list_clear = []
    image_list_dirty = []
    path = ['Images']
    for file_name in os.listdir(os.path.join(*path)):
        path.append(file_name)
        img = Image.open(os.path.join(*path))
        arr = np.array(img)
        img.close()
        if file_name[:5] == 'dirty':
            image_list_dirty.append(arr)
        else:
            image_list_clear.append(arr)

        path.pop()
    return image_list_clear, image_list_dirty


def global_binary(img):
    image = cv2.imread(f'Images/dirty_{img}.jpg', cv2.IMREAD_GRAYSCALE)
    threshold_value = 128

    binary_image = np.where(image >= threshold_value, 255, 0)
    return binary_image


def global_otsu(img):
    image = cv2.imread(f'Images/dirty_{img}.jpg', cv2.IMREAD_GRAYSCALE)

    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary_image


def gaussian_blur(img):
    image = cv2.imread(f'Images/dirty_{img}.jpg')

    kernel_size = (5, 5)
    sigma = 0

    smoothed_image = cv2.GaussianBlur(image, kernel_size, sigma)
    return smoothed_image


def average_blur(img):
    image = cv2.imread(f'Images/dirty_{img}.jpg')

    kernel_size = (5, 5)

    smoothed_image = cv2.blur(image, kernel_size)
    return smoothed_image


def save_images(indx):
    image_list_clear, image_list_dirty = init()

    path1 = 'static/trash/img.jpeg'
    path2 = 'static/trash/img1.jpeg'
    path3 = 'static/trash/img3.jpeg'
    path4 = 'static/trash/img4.jpeg'
    path5 = 'static/trash/img5.jpeg'

    img1 = cv2.imread(f'Images/dirty_{indx}.jpg')
    cv2.imwrite(path1, img1)

    img2 = global_binary(indx)
    cv2.imwrite(path2, img2)
    # global_binary(image_list_dirty[indx])

    img3 = global_otsu(indx)
    cv2.imwrite(path3, img3)

    img4 = gaussian_blur(indx)
    cv2.imwrite(path4, img4)

    img5 = average_blur(indx)
    cv2.imwrite(path5, img5)

    return [
        'trash/img.jpeg',
        'trash/img1.jpeg',
        'trash/img3.jpeg',
        'trash/img4.jpeg',
        'trash/img5.jpeg'
    ]


ind = 1


@app.route('/', methods=['GET', 'POST'])
def index():
    global ind
    images = save_images(ind)

    if request.method == 'POST':
        ind = int(request.json['inputField'])
        print(ind)
        images = save_images(ind)
        return render_template('index.html', images=images)

    return render_template('index.html', images=images)


if __name__ == '__main__':
    app.run()
