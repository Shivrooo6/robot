import numpy as np
import librosa
import joblib

# Load your trained model
model = joblib.load('emotion_model.pkl')

# Path to your test audio file
audio_path = 'test_audio.wav'

# Preprocess: Extract MFCC features
def extract_features(path):
    y, sr = librosa.load(path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfcc_scaled = np.mean(mfcc.T, axis=0)  # shape: (40,)
    return mfcc_scaled.reshape(1, -1)       # shape: (1, 40)

# Predict emotion
features = extract_features(audio_path)
prediction = model.predict(features)[0]
proba = model.predict_proba(features)

print(f"Predicted Emotion: {prediction}")
print("Confidence per class:")
for label, score in zip(model.classes_, proba[0]):
    print(f" - {label}: {score:.2f}")
try:
    print("🔍 Loading model...")
    model = joblib.load('emotion_model.pkl')
    
    print("🎧 Loading audio...")
    y, sr = librosa.load('test_audio.wav', sr=16000)
    
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfcc_scaled = np.mean(mfcc.T, axis=0).reshape(1, -1)
    
    print("🧠 Predicting emotion...")
    prediction = model.predict(mfcc_scaled)[0]
    proba = model.predict_proba(mfcc_scaled)[0]
    
    print(f"\n🎤 Predicted Emotion: {prediction}")
    print("Confidence per class:")
    for label, score in zip(model.classes_, proba):
        print(f" - {label}: {score:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")
