import tensorflow as tf
import numpy as np
import os

# Ensure model folder exists
os.makedirs("model", exist_ok=True)

# Dummy dataset: 100 samples, 20 features
X = np.random.rand(100, 20)
y = np.random.randint(0, 2, size=(100,))

# Simple binary classification model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(20,)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X, y, epochs=5, batch_size=8, verbose=1)

# Save model
model.save("model/garbage_model.h5")
print("✅ Model saved to model/garbage_model.h5")
