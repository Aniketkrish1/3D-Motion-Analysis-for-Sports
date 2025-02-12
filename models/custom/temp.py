import json
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import OneHotEncoder

# Load the trained model
model = load_model("posture_analysis_model.h5")

# Load encoders from training phase
with open("../../data/synthetic_landmarks/landmarks.json", "r") as f:
    data = json.load(f)

sports = [entry["sport"] for entry in data]
labels = [entry["label"] for entry in data]

encoder_sport = OneHotEncoder().fit(np.array(sports).reshape(-1, 1))
encoder_label = OneHotEncoder().fit(np.array(labels).reshape(-1, 1))

# Predict function
def predict_posture_for_video(landmarks_file, sport):
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
        # Ensure frame_landmarks is a list of dictionaries with keys "x", "y", "z"
        if isinstance(frame_landmarks, list):
            try:
                # Ensure the correct number of landmarks (25 landmarks with x, y, z coordinates)
                if len(frame_landmarks) != 25:
                    # print(f"Warning: Expected 25 landmarks, but got {len(frame_landmarks)} landmarks. Truncating or padding.")
                    # Adjust if the number of landmarks is more or less than expected
                    if len(frame_landmarks) > 25:
                        frame_landmarks = frame_landmarks[:25]  # Truncate
                    elif len(frame_landmarks) < 25:
                        # Pad with zeros if there are fewer landmarks (not ideal, but can be a fallback)
                        frame_landmarks += [{"x": 0, "y": 0, "z": 0}] * (25 - len(frame_landmarks))

                # Flatten landmarks for the current frame (25 landmarks * 3 coordinates)
                flat_landmarks = [coord for point in frame_landmarks for coord in (point["x"], point["y"], point["z"])]
                
                # Ensure flat_landmarks has 75 features (25 * 3)
                if len(flat_landmarks) != 75:
                    # print(f"Error: Expected 75 features from landmarks, got {len(flat_landmarks)}.")
                    continue
                
                # Reshape flat_landmarks to be a 2D array (1, -1) for compatibility with sport_encoded
                flat_landmarks = np.array(flat_landmarks).reshape(1, -1)
                
                # Combine landmarks and sport encoding for this frame (Total should be 82 features)
                input_data = np.hstack([flat_landmarks, sport_encoded])
                
                # Check the shape of the input data
                if input_data.shape[1] != 82:
                    # print(f"Error: Expected input data with 82 features, got {input_data.shape[1]} features.")
                    continue
                
                # Make prediction for this frame
                prediction = model.predict(input_data)
                label = encoder_label.inverse_transform(prediction)
                current_recommendation = label[0][0]

                # Check if recommendation has changed
                if current_recommendation != previous_recommendation:
                    if previous_recommendation is not None:
                        # Print range and previous recommendation
                        print(f"Frame {start_frame}-{frame_idx - 1}: Recommended action: {previous_recommendation}")
                    # Update start frame and previous recommendation
                    start_frame = frame_idx
                    previous_recommendation = current_recommendation

            except (KeyError, TypeError):
                print(f"Skipping frame due to invalid landmark data: {frame_landmarks}")
                continue
        else:
            print(f"Skipping invalid frame data: {frame_landmarks}")
            continue
    
    # Print the final range
    if previous_recommendation is not None:
        print(f"Frame {start_frame}-{len(landmarks_video)}: Recommended action: {previous_recommendation}")

    return recommendations

# Example input for prediction: landmarks file path and sport
landmarks_file = "../../data/landmark_analysis/cric_sample1.mp4.json"
sport = "golf"

# Predict and print recommendations for the entire video
recommendations = predict_posture_for_video(landmarks_file, sport)
for idx, rec in enumerate(recommendations):
    print(f"Frame {idx + 1}: Recommended action: {rec}")
