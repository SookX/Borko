import numpy as np
import librosa

def preprocess_wav(file_path, sample_rate=16000, frame_size=0.02, frame_stride=0.01):
    """
    Preprocesses a .wav file for a Deep Speech-like speech recognition pipeline.

    Args:
        file_path (str): Path to the .wav file.
        sample_rate (int): Target sampling rate. Defaults to 16 kHz.
        frame_size (float): Frame size in seconds. Defaults to 20ms.
        frame_stride (float): Frame stride in seconds. Defaults to 10ms.

    Returns:
        np.ndarray: Processed spectrogram features.
    """
    # Load the audio file
    audio, sr = librosa.load(file_path, sr=sample_rate)
    
    # Compute Short-Time Fourier Transform (STFT)
    n_fft = int(sample_rate * frame_size)  # Number of FFT components
    hop_length = int(sample_rate * frame_stride)  # Hop length (stride)
    stft = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length, win_length=n_fft, window='hamming')
    
    # Compute spectrogram (power of STFT magnitude)
    spectrogram = np.abs(stft) ** 2
    
    # Compute log filter bank features
    log_filter_banks = librosa.feature.melspectrogram(S=spectrogram, sr=sample_rate, n_mels=80)
    log_filter_banks = np.log(log_filter_banks + 1e-6)  # Add a small value to avoid log(0)
    
    # Normalize features
    mean = np.mean(log_filter_banks, axis=0)
    std = np.std(log_filter_banks, axis=0)
    normalized_features = (log_filter_banks - mean) / std
    
    return normalized_features

def add_context(frames, context_size=9):
    """
    Adds context frames to the input features.

    Args:
        frames (np.ndarray): Input feature frames.
        context_size (int): Number of frames to include before and after the current frame.

    Returns:
        np.ndarray: Features with context.
    """
    padded_frames = np.pad(frames, ((context_size, context_size), (0, 0)), mode='constant')
    context_features = np.lib.stride_tricks.sliding_window_view(padded_frames, window_shape=(context_size * 2 + 1, frames.shape[1]))
    return context_features.reshape(frames.shape[0], -1)

# Add context to features
