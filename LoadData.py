import os
import numpy as np
from skimage import io, transform, img_as_ubyte,color


def scan_files(directory, prefix=None, postfix='.jpg'):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(os.path.abspath(directory), special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(os.path.abspath(directory), special_file))
            else:
                files_list.append(os.path.join(os.path.abspath(directory), special_file))
    return files_list

def image_norm(image, image_size):
    return img_as_ubyte(transform.resize(image, image_size))

def get_photo_data(file, image_size=(224, 224)):
    data = []
    try:
        img = io.imread(file[0])
        img = color.gray2rgb(img)  # 软件保存的图是二维的
        img = image_norm(img, image_size)
    except:
        print('Load', file, 'fail')
        return
    if img.shape != (image_size[0], image_size[1], 3):
        return
    data.append(img)
    data = np.array(data)
    return data

def load_data(path):
    X = get_photo_data(scan_files(path))
    return X


