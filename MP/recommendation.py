import json
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import OneHotEncoder

# Load the trained model
model = load_model("../models/custom/posture_analysis_model.h5")

# Load encoders from training phase
with open("../data/synthetic_landmarks/landmarks.json", "r") as f:
    data = json.load(f)

sports = [entry["sport"] for entry in data]
labels = [entry["label"] for entry in data]

encoder_sport = OneHotEncoder().fit(np.array(sports).reshape(-1, 1))
encoder_label = OneHotEncoder().fit(np.array(labels).reshape(-1, 1))

# Predict function
def recommend(landmarks_file, sport):
    # Load landmarks from the JSON file
    with open(landmarks_file, "r") as f:
        landmarks_video = json.load(f)  # This should load the list of frames
    
    recommendations = []
    frame_ranges = []
    previous_recommendation = None
    start_frame = 1

    # One-hot encode the sport
    sport_encoded = encoder_sport.transform([[sport]]).toarray()

    for frame_idx, frame_landmarks in enumerate(landmarks_video, start=1):
        if isinstance(frame_landmarks, list):
            try:
                # Ensure correct number of landmarks
                if len(frame_landmarks) != 25:
                    if len(frame_landmarks) > 25:
                        frame_landmarks = frame_landmarks[:25]  # Truncate
                    elif len(frame_landmarks) < 25:
                        frame_landmarks += [{"x": 0, "y": 0, "z": 0}] * (25 - len(frame_landmarks))

                # Flatten landmarks
                flat_landmarks = [coord for point in frame_landmarks for coord in (point["x"], point["y"], point["z"])]
                if len(flat_landmarks) != 75:
                    continue

                # Combine landmarks and sport encoding
                flat_landmarks = np.array(flat_landmarks).reshape(1, -1)
                input_data = np.hstack([flat_landmarks, sport_encoded])
                if input_data.shape[1] != 82:
                    continue

                # Make prediction
                prediction = model.predict(input_data)
                label = encoder_label.inverse_transform(prediction)
                current_recommendation = label[0][0]

                # Record recommendation
                if current_recommendation != previous_recommendation:
                    if previous_recommendation is not None:
                        recommendations.append({
                            "frame_range": f"{start_frame}-{frame_idx - 1}",
                            "action": previous_recommendation
                        })
                    start_frame = frame_idx
                    previous_recommendation = current_recommendation

            except (KeyError, TypeError):
                print(f"Skipping frame due to invalid landmark data: {frame_landmarks}")
                continue
        else:
            print(f"Skipping invalid frame data: {frame_landmarks}")
            continue
    
    # Add the final recommendation
    if previous_recommendation is not None:
        recommendations.append({
            "frame_range": f"{start_frame}-{len(landmarks_video)}",
            "action": previous_recommendation
        })

    return recommendations
