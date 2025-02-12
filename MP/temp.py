import cv2
import mediapipe as mp

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB (Mediapipe expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect joints
    results = pose.process(rgb_frame)

    # Draw landmarks and connections
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )

    # Display the result
    cv2.imshow('Pose Detection', frame)

    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
