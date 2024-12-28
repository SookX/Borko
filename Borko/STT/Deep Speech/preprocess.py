import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np


file = 'hadji_dimitur.wav'
signal, sr = librosa.load(file, sr = 22050) # sr * T -> 22050 * 13
#librosa.display.waveshow(signal, sr = sr)
#plt.xlabel("Time")
#plt.ylabel("Amplitude")
#plt.show()

fft = np.fft.fft(signal)
mag = np.abs(fft)
frequency = np.linspace(0, sr, len(mag))

left_frequency = frequency[:int(len(frequency) / 2)]
left_magnitude = mag[:int(len(frequency) / 2)]

#plt.plot(left_frequency, left_magnitude)
#plt.xlabel("Frequency")
#plt.ylabel("Magnitude")
#plt.show()

n_fft = 2048
hop_length = 512
stft = librosa.core.stft(signal, hop_length=hop_length, n_fft=n_fft)
spectogram = np.abs(stft)

log_spectogram = librosa.amplitude_to_db(spectogram)

#librosa.display.specshow(log_spectogram, sr=sr, hop_length=hop_length)
#plt.xlabel("Time")
#plt.ylabel("Frequency")
#plt.colorbar()
#plt.show()

MFFCs = librosa.feature.mfcc(signal, n_fft = n_fft, hop_length = hop_length, n_mfcc=13)
librosa.display.specshow(MFFCs, sr=sr, hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("MFCC")
plt.colorbar()
plt.show()
