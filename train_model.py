import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import joblib

# Simulated MFCC features: 100 samples with 40 features each
X = np.random.rand(100, 40)

# Simulated labels: 4 emotions (25 of each)
y = ['happy'] * 25 + ['sad'] * 25 + ['angry'] * 25 + ['neutral'] * 25
y = np.array(y)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple SVM model
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'emotion_model.pkl')
print("✅ Model saved as emotion_model.pkl")
