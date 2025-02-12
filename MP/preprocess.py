# import cv2

# def preprocess_video(input_path, output_path):
#     cap = cv2.VideoCapture(input_path)

#     if not cap.isOpened():
#         raise FileNotFoundError(f"Could not open video: {input_path}")

#     fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use XVID codec for compatibility
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))

#     out = cv2.VideoWriter(output_path, fourcc, fps, (1280, 720))  # Resize to 720p

#     while cap.isOpened():
#         ret, frame = cap.read()
#         # if not ret:
#         #     print("End of video or no frames to read.")
#         #     break

#         # print(f"Processing frame of size: {frame.shape}")  # Debug frame size
#         frame_resized = cv2.resize(frame, (1280, 720))  # Resize to 720p
#         out.write(frame_resized)

#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
#     print(f"Video saved at: {output_path}")

import cv2
import os

def preprocess_video(input_video_path, output_video_path):
    # Check the file extension
    file_extension = os.path.splitext(input_video_path)[-1].lower()
    if file_extension not in ['.mp4', '.avi']:
        raise ValueError("Unsupported file format! Please upload an .mp4 or .avi file.")
    
    # Open the video file using OpenCV
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video file: {input_video_path}")
    
    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Process video frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Example preprocessing: Convert frame to grayscale
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)  # Convert back to 3-channel
        out.write(processed_frame)
    
    # Release resources
    cap.release()
    out.release()
