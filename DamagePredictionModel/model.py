import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import VGG19
from tensorflow.keras.optimizers import Adam

# Load the VGG19 model pre-trained on ImageNet (without the top layers)
base_model = VGG19(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Add custom layers on top for damage classification
x = base_model.output
x = GlobalAveragePooling2D()(x)  # Global Average Pooling to reduce dimensions
x = Dense(1024, activation='relu')(x)  # Fully connected layer
x = Dense(1, activation='sigmoid')(x)  # Output layer (1 for binary classification)

# Create the full model
model = Model(inputs=base_model.input, outputs=x)

# Freeze the base VGG19 layers to retain pre-trained features
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

# Optionally, you can train this model on your car damage dataset or use it for inference
model.summary()
