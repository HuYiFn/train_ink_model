from keras.models import Model, load_model
import numpy as np
from LoadData import load_data
import gc
import random
from keras.applications.mobilenet import relu6,DepthwiseConv2D
import datetime
from keras.preprocessing import image
gc.collect()
import numpy as np
from skimage import io, transform, img_as_ubyte
import os
lst = ['鸟','荷','竹','马','菊','兰','柳','梅','山']
starttime = datetime.datetime.now()
X_test, Y_test = load_data('E:\\Qianrushi\\test')

image_size=(224, 224)

X_test = X_test.astype('float32')
X_test /= 255.

X_test -= 0.5

X_test *= 2.


model = load_model('mobilenet1.hdf5',custom_objects={
                  'relu6': relu6,
                  'DepthwiseConv2D': DepthwiseConv2D})

# model = load_model('finalvgg16.hdf5')



predict_list = model.predict(X_test)
print(lst[np.argmax(predict_list)])

# for i in range(len(Y_test)):
#     if np.argmax(predict_list[i]) == np.argmax(Y_test[i]):
        # print(np.argmax(predict_list[i]))
        # count +=1
# print(count/len(Y_test))
endtime = datetime.datetime.now()
print(endtime-starttime)
#scores = model.evaluate(X_test,Y_test,verbose=0)
#print(scores)