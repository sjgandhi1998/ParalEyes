import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from keras.applications import VGG16 
from keras.preprocessing.image import ImageDataGenerator

#Load the VGG model
image_size1 = 60
image_size2 = 90
vgg_conv = VGG16(weights='imagenet', 
                 include_top=False, 
                 input_shape=(image_size1, image_size2, 3))

# Freeze the layers except the last 4 layers
for layer in vgg_conv.layers[:-4]:
    layer.trainable = False
    
# Check the trainable status of the individual layers
for layer in vgg_conv.layers:
    print(layer, layer.trainable)
    
from keras import models
from keras import layers
from keras import optimizers

# Create the model
model = models.Sequential()

# Add the vgg convolutional base model
model.add(vgg_conv)

# Add new layers
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(5, activation='softmax'))

# Show a summary of the model. Check the number of trainable params
model.summary()
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

validation_datagen = ImageDataGenerator(rescale=1./255)

#Change the batchsize according to the system RAM
train_batchsize = 100
val_batchsize = 10

train_dir='C:/Users/Sjgandhi1998/Software/Data/ParalEyes/training_data/train'
validation_dir='C:/Users/Sjgandhi1998/Software/Data/ParalEyes/training_data/validation'

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(image_size1, image_size2),
    batch_size=train_batchsize,
    class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(image_size1, image_size2),
    batch_size=val_batchsize,
    class_mode='categorical',
    shuffle=False)

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])


# Train the model
history = model.fit_generator(
    generator=train_generator,
    steps_per_epoch=train_generator.samples//train_generator.batch_size,
    epochs=30,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples//validation_generator.batch_size,
    verbose=1)

# Save the model
model.save('small_last4.h5')

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

import matplotlib.pyplot as plt

plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
