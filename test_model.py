import numpy as np
import librosa
from tensorflow.keras.models import load_model

model = load_model('model.h5')  # path to your trained model

labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']

def preprocess_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    return np.expand_dims(mfcc_mean, axis=0)

def predict(audio_path):
    input_data = preprocess_audio(audio_path)
    prediction = model.predict(input_data)
    predicted_index = np.argmax(prediction)
    predicted_label = labels[predicted_index]
    print(f"Prediction: {predicted_label} ({prediction[0][predicted_index]:.2f} confidence)")

predict('test_audio.wav')  # change this if needed
