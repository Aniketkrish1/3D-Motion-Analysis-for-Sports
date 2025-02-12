import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Load Video
video_path = "../videos/15172075-uhd_2160_3840_60fps.mp4"  # Use the correct path with forward slashes
cap = cv2.VideoCapture(video_path)

# Check if video is opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Desired output dimensions for resizing
output_width, output_height = 640, 480  # Example resolution
blank_frame_color = (0, 0, 0)  # Background color for skeleton-only frames (black)

# Initialize VideoWriter to save both full-frame and skeleton-only videos
output_full_video = cv2.VideoWriter(
    "output_with_keypoints.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (output_width, output_height)
)
output_skeleton_video = cv2.VideoWriter(
    "output_skeleton_only.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (output_width, output_height)
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to fit the desired resolution
    resized_frame = cv2.resize(frame, (output_width, output_height))

    # Convert the resized frame to RGB (for Mediapipe)
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    # Detect Pose
    results = pose.process(rgb_frame)

    # Create a blank frame for the skeleton-only visualization
    skeleton_frame = np.zeros((output_height, output_width, 3), dtype=np.uint8)  # Blank black frame

    # Draw keypoints and connections
    if results.pose_landmarks:
        # Draw keypoints and connections on the resized full-frame
        mp_drawing.draw_landmarks(resized_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Draw keypoints and connections on the skeleton-only frame
        mp_drawing.draw_landmarks(skeleton_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Write both full-frame and skeleton-only videos
    output_full_video.write(resized_frame)
    output_skeleton_video.write(skeleton_frame)

    # Show frames (Optional)
    cv2.imshow('Pose Detection - Full Frame', resized_frame)
    cv2.imshow('Pose Detection - Skeleton Only', skeleton_frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
output_full_video.release()
output_skeleton_video.release()
cv2.destroyAllWindows()
