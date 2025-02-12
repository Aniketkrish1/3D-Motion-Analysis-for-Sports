# import mediapipe as mp
# import cv2
# import json

# mp_pose = mp.solutions.pose

# def extract_landmarks(input_video_path, output_path):
#     cap = cv2.VideoCapture(input_video_path)
#     if not cap.isOpened():
#         raise FileNotFoundError(f"Could not open video: {input_video_path}")

#     pose = mp_pose.Pose()
#     all_landmarks = []

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(frame_rgb)

#         if results.pose_landmarks:
#             landmarks = [
#                 {"x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility}
#                 for lm in results.pose_landmarks.landmark
#             ]
#             all_landmarks.append(landmarks)

#     cap.release()

#     with open(output_path, "w") as f:
#         json.dump(all_landmarks, f)




import json
import numpy as np
import mediapipe as mp
import cv2


mp_pose = mp.solutions.pose
# Extract landmarks (dummy implementation with placeholder data)
def extract_landmarks(input_video_path, output_json_path):
    """
    Extract pose landmarks from a video using MediaPipe Pose and save them to a JSON file.

    Parameters:
    - input_video_path: Path to the input video file.
    - output_json_path: Path where the extracted landmarks will be saved as a JSON file.
    """
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {input_video_path}")

    pose = mp_pose.Pose()
    landmarks_data = []  # To store the landmarks for each frame

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Exit when video frames are exhausted

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Check if pose landmarks are detected
        if results.pose_landmarks:
            # Extract landmarks into a list of dictionaries
            frame_landmarks = [
                {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z,
                    "visibility": lm.visibility,
                }
                for lm in results.pose_landmarks.landmark
            ]
            landmarks_data.append(frame_landmarks)

    # Save landmarks to a JSON file
    with open(output_json_path, "w") as f:
        json.dump(landmarks_data, f)

    cap.release()

import json
import numpy as np

def analyze_sport(landmarks_path, sport):
    try:
        # Load the data
        with open(landmarks_path, "r") as f:
            data = json.load(f)

        # Convert to a NumPy array for easier processing
        keypoints = np.array([[list(kp.values())[:3] for kp in frame] for frame in data])  # Extract x, y, z
        num_frames, num_keypoints, _ = keypoints.shape

        # Calculate distances between consecutive frames
        distances = np.linalg.norm(keypoints[1:] - keypoints[:-1], axis=2)  # Shape: (frames-1, keypoints)
        avg_speed = np.mean(distances)  # Mean speed over all frames

        # Sport-specific recommendations (examples)
        recommendations = {
            "golf": [
                "Ensure your knees are slightly bent during setup.",
                "Maintain a smooth backswing and downswing.",
                "Focus on a strong follow-through for consistent shots."
            ],
            "cricket": [
                "Keep your eyes on the ball at all times.",
                "Ensure your front knee is bent while playing a drive.",
                "Improve foot movement to get into better positions."
            ],
            "default": ["Maintain consistent posture and timing."]
        }

        # Compile the analysis results
        analysis_results = {
            "Sport": sport.capitalize(),
            "Total Frames": num_frames,
            "Key Points Tracked": num_keypoints,
            "Average Speed (units/frame)": round(avg_speed, 2),
        }

        return analysis_results,recommendations

    except Exception as e:
        return {"error": str(e)}



# extract_landmarks("../data/raw/golf_sample1.avi", "../data/landmarks/landmarks.json")
def landmarks(input_video_path, output_json_path):
    """
    Extract pose landmarks from a video using MediaPipe Pose and save them to a JSON file.

    Parameters:
    - input_video_path: Path to the input video file.
    - output_json_path: Path where the extracted landmarks will be saved as a JSON file.
    """
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {input_video_path}")

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    landmarks_data = []  # To store the landmarks for each frame

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Exit when video frames are exhausted

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Check if pose landmarks are detected
        if results.pose_landmarks:
            # Extract landmarks into a list of dictionaries
            frame_landmarks = [
                {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z,
                    "visibility": lm.visibility,
                }
                for lm in results.pose_landmarks.landmark
            ]
            landmarks_data.append(frame_landmarks)

    # # Debug: Print sample data
    # if landmarks_data:
    #     print("Sample Landmarks Data:", json.dumps(landmarks_data[:2], indent=4))

    # Save landmarks to a JSON file
    with open(output_json_path, "w") as f:
        json.dump(landmarks_data, f)

    cap.release()


def analyze_posture(landmarks_path, sport):
    # Load and parse JSON file
    with open(landmarks_path, "r") as f:
        data = json.load(f)

    # Validate structure
    if not isinstance(data, list) or len(data) == 0 or not isinstance(data[0], list):
        raise ValueError("Invalid data format: Expected a list of frames, each containing keypoints.")

    # Access the first frame for analysis
    first_frame = data[0]  # Assuming data[0] contains the keypoints for the first frame

    try:
        # Extract common landmarks (indices may vary based on model)
        left_knee = np.array([first_frame[23]["x"], first_frame[23]["y"], first_frame[23]["z"]])
        left_hip = np.array([first_frame[11]["x"], first_frame[11]["y"], first_frame[11]["z"]])
        left_ankle = np.array([first_frame[25]["x"], first_frame[25]["y"], first_frame[25]["z"]])
        right_shoulder = np.array([first_frame[12]["x"], first_frame[12]["y"], first_frame[12]["z"]])
        left_shoulder = np.array([first_frame[11]["x"], first_frame[11]["y"], first_frame[11]["z"]])
        torso_midpoint = (left_shoulder + right_shoulder) / 2
    except (IndexError, KeyError, TypeError) as e:
        raise ValueError("Invalid landmark format. Ensure the JSON structure matches the expected format.") from e

    # Calculate knee angle using vector math
    vector_hip_knee = left_knee - left_hip
    vector_knee_ankle = left_ankle - left_knee
    cosine_angle = np.dot(vector_hip_knee, vector_knee_ankle) / (
        np.linalg.norm(vector_hip_knee) * np.linalg.norm(vector_knee_ankle)
    )
    knee_angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    # Calculate torso lean angle
    torso_vector = left_hip - torso_midpoint
    vertical_vector = np.array([0, 1, 0])
    cosine_torso_angle = np.dot(torso_vector, vertical_vector) / (np.linalg.norm(torso_vector) * np.linalg.norm(vertical_vector))
    torso_angle = np.degrees(np.arccos(np.clip(cosine_torso_angle, -1.0, 1.0)))

    # Generate sport-specific recommendations and insights
    recommendations = []
    insights = {}

    if sport.lower() == "basketball":
        if knee_angle < 80:
            recommendations.append("Bend your knees more for better shooting balance.")
        elif knee_angle > 150:
            recommendations.append("Avoid locking your knees while preparing to jump.")
        else:
            recommendations.append("Good posture for shooting or defense.")
        if torso_angle > 20:
            recommendations.append("Keep your torso upright for better control.")
        insights["tip"] = "Maintain a low stance for effective defense and balance during shooting."

    elif sport.lower() == "yoga":
        if knee_angle < 70:
            recommendations.append("Engage your core and balance your stance.")
        elif knee_angle > 160:
            recommendations.append("Ensure your knee alignment is stable in the pose.")
        else:
            recommendations.append("Excellent posture for this yoga pose.")
        if torso_angle > 10:
            recommendations.append("Keep your torso aligned with your hips for better stability.")
        insights["tip"] = "Focus on breathing and symmetry for improved balance."

    elif sport.lower() == "running":
        if knee_angle < 60:
            recommendations.append("Shorten your stride to avoid overstriding.")
        elif knee_angle > 140:
            recommendations.append("Ensure a natural knee bend while running.")
        else:
            recommendations.append("Great posture for efficient running mechanics.")
        if torso_angle > 15:
            recommendations.append("Avoid leaning too far forward to prevent fatigue.")
        insights["tip"] = "Maintain a steady cadence and relaxed upper body for better performance."

    elif sport.lower() == "soccer":
        if knee_angle < 75:
            recommendations.append("Stay low for better ball control and agility.")
        elif knee_angle > 155:
            recommendations.append("Avoid overextending your knees during kicks.")
        else:
            recommendations.append("Optimal knee angle for movement and stability.")
        if torso_angle > 20:
            recommendations.append("Keep your torso balanced for quick direction changes.")
        insights["tip"] = "Adapt your posture for precise kicks and effective defense."

    elif sport.lower() == "tennis":
        if knee_angle < 80:
            recommendations.append("Bend your knees more for better lateral movement.")
        elif knee_angle > 150:
            recommendations.append("Avoid straightening your knees too much during volleys.")
        else:
            recommendations.append("Good posture for effective court coverage.")
        if torso_angle > 18:
            recommendations.append("Keep your torso aligned for powerful strokes.")
        insights["tip"] = "Stay on the balls of your feet for agility and quick reactions."

    elif sport.lower() == "cricket":
        if knee_angle < 75:
            recommendations.append("Bend your knees more for stability during batting or bowling.")
        elif knee_angle > 155:
            recommendations.append("Avoid locking your knees while fielding or bowling.")
        else:
            recommendations.append("Optimal posture for cricket movements.")
        if torso_angle > 20:
            recommendations.append("Keep your torso balanced for effective movement.")
        insights["tip"] = "Maintain a balanced stance for better performance in batting and bowling."

    elif sport.lower() == "golf":
        if knee_angle < 70:
            recommendations.append("Bend your knees slightly more for a stable swing.")
        elif knee_angle > 160:
            recommendations.append("Avoid overextending your knees during the swing.")
        else:
            recommendations.append("Good posture for a controlled golf swing.")
        if torso_angle > 15:
            recommendations.append("Keep your torso aligned for a smooth swing motion.")
        insights["tip"] = "Focus on maintaining balance and a consistent swing path."

    else:
        recommendations.append("Sport not recognized. Default analysis applied.")
        insights["tip"] = "Provide a valid sport for tailored insights."

    keypoints = np.array([[list(kp.values())[:3] for kp in frame] for frame in data])
    distances = np.linalg.norm(keypoints[1:] - keypoints[:-1], axis=2)  # Shape: (frames-1, keypoints)
    avg_speed = np.mean(distances) 
    return [round(knee_angle,2),round(torso_angle,2),avg_speed]

print(analyze_posture("../data/landmarks/golf_sample1.avi.json","golf"))