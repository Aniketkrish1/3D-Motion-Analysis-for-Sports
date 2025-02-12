import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Load synthetic data
with open("../../data/synthetic_landmarks/landmarks.json", "r") as f:
    data = json.load(f)

# Prepare features and labels
X = []
y = []
sports = []

for entry in data:
    landmarks = entry["landmarks"]
    sport = entry["sport"]
    label = entry["label"]

    # Flatten landmark coordinates
    flat_landmarks = [coord for point in landmarks for coord in (point["x"], point["y"], point["z"])]
    X.append(flat_landmarks)
    y.append(label)
    sports.append(sport)

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)
sports = np.array(sports)

# One-hot encode sports and labels
encoder_sport = OneHotEncoder()
encoder_label = OneHotEncoder()

sports_encoded = encoder_sport.fit_transform(sports.reshape(-1, 1)).toarray()
labels_encoded = encoder_label.fit_transform(y.reshape(-1, 1)).toarray()

# Combine features (landmarks + sports encoding)
X_combined = np.hstack([X, sports_encoded])

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_combined, labels_encoded, test_size=0.2, random_state=42)

# Define a simple neural network model
model = Sequential([
    Dense(128, activation="relu", input_shape=(X_combined.shape[1],)),
    Dropout(0.2),
    Dense(64, activation="relu"),
    Dropout(0.2),
    Dense(labels_encoded.shape[1], activation="softmax"),
])

# Compile the model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Save the model
model.save("posture_analysis_model.h5")
print("Model trained and saved as 'posture_analysis_model.h5'.")
