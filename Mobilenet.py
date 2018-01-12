import ImageProcess
from keras.applications.mobilenet import MobileNet
from keras.layers import Input,Flatten,Dense,Dropout,GlobalAveragePooling2D
from keras.models import Model
from keras.optimizers import SGD
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping, TensorBoard, ModelCheckpoint
import numpy as np

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5
set_session(tf.Session(config=config))
batch_size = 32
num_classes = 9
epochs = 200
data_augmentation = False
#num_predictions = 20

lr_reducer = ReduceLROnPlateau(factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
early_stopper = EarlyStopping(min_delta=0.0001, patience=10)
csv_logger = CSVLogger('final.csv')
tensor_board = TensorBoard(log_dir='./logs', histogram_freq=0)
checkpointer = ModelCheckpoint(filepath="mobilenet.hdf5", verbose=1, save_best_only=True)

# input image dimensions
img_rows, img_cols = 299, 299
# The images are RGB.
img_channels = 3

# The data, shuffled and split between train and test sets:
(X_train, Y_train)= ImageProcess.load_data(r'../newdecolor2rgb')

X_train = X_train.astype('float32')
#X_test = X_test.astype('float32')

X_train /= 255.
#X_test /= 255.
X_train -= 0.5
#X_test -= 0.5
X_train *= 2.
#X_test *= 2.

model_mobilenet = MobileNet(include_top=False,weights='imagenet',input_shape=(224,224,3))
for layer in model_mobilenet.layers:
    layer.trainable = False
x = model_mobilenet.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(12, activation='sigmoid')(x)
model = Model(inputs=model_mobilenet.input, outputs=predictions)
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
# model = Flatten()(model_mobilenet.output)
# model = Dense(9,activation='softmax')(model)
# model_mobilenet_ink_pretrain = Model(model_mobilenet.input,model)
#
# model_mobilenet_ink_pretrain.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

if not data_augmentation:
    print('Not using data augmentation.')
    model.fit(X_train, Y_train,
              batch_size=batch_size,
              epochs=epochs,
              shuffle=True,
              callbacks=[lr_reducer, csv_logger, tensor_board, checkpointer])

else:
    print('Using real-time data augmentation.')
    # This will do preprocessing and realtime data augmentation:
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    # Compute quantities required for feature-wise normalization
    # (std, mean, and principal components if ZCA whitening is applied).
    datagen.fit(X_train)
    model.fit_generator(datagen.flow(X_train, Y_train,
                                     batch_size=batch_size),
                        steps_per_epoch=X_train.shape[0] // batch_size,
                        epochs=epochs,
                        #validation_data=(X_test, Y_test),
                        workers=4)
model.save('mobilenet.hdf5')
