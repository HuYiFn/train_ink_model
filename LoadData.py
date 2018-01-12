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
    print(len(files_list))
    return files_list

def image_norm(image, image_size):
    return img_as_ubyte(transform.resize(image, image_size))

def filename_to_label(file):
   # lst = ['梅','菊','竹','山','柳','鸟','荷','兰','马']
    lst = ['bird','he','zhu','horse','ju','lan','liu','mei','mountain']
    name = os.path.basename(file)
    label = np.zeros(len(lst))
    for i in range(len(lst)):
        if lst[i] in name:
            label[i] = 1
            #print(lst[i])
    return  label

def get_photo_data(file_list, image_size=(224, 224)):
    data, Label = [], []
    source = file_list
    # lock = threading.Lock()
    def work(i):
        file = source.pop(0)
        try:
            img = io.imread(file)
            img = color.gray2rgb(img)    #软件保存的图是二维的
            img = image_norm(img, image_size)
            label = filename_to_label(file)
        except:
            print('Load', file, 'fail')
            return
        if img.shape != (image_size[0], image_size[1], 3):
            #newimg = color.gray2rgb(img)
            #img = newimg
            return

        data.append(img)
        Label.append(label)

    for _ in range(len(source)):
        work(_)
    data = np.array(data)
    Label = np.array(Label)
    assert data.shape[0] == Label.shape[0]
    print(data.shape, Label.shape)
    return data, Label

def load_data(path):
    import random

    X, Y = get_photo_data(scan_files(path))

    Len = X.shape[0]
    index = [i for i in range(Len)]
    random.shuffle(index)
    X = X[index]
    Y = Y[index]

    return X,Y


