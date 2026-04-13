import os
import numpy as np
from openwakeword.train import train_model

# Training configuration
train_model(
    positive_samples="wakeword_samples/ada",
    output_dir="wakeword_model",
    model_name="ada",
    epochs=100,
    batch_size=32
)

print("Training complete! Model saved to wakeword_model/")