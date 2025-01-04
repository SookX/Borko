import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import preprocess_wav, add_context

#print(os.getcwd())
file = 'hadji_dimitur.wav'
features = preprocess_wav(file)
print("Preprocessed Features Shape:", features.shape)

context_features = add_context(features, context_size=9)
print("Context Features Shape:", context_features.shape)

