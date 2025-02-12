import streamlit as st
import os
import cv2
from main import process_video_pipeline
import mediapipe as mp
# Ensure required directories exist
# os.makedirs("data/raw", exist_ok=True)
# os.makedirs("outputs/animations", exist_ok=True)
# os.makedirs("outputs/reports", exist_ok=True)

st.title("Sports Motion Analysis")
st.write(
    """
    Upload a sports video, capture from webcam, select the sport type, and get a detailed analysis report along with 3D animations!
    """
)

# Select input type
input_type = st.radio("Choose input type:", ("Upload Video", "Webcam"))

# Common sport selection
selected_sport = st.selectbox(
    "Select the sport for analysis",
    ["Running", "Basketball", "Tennis", "Yoga", "Cricket", "Golf"],
)

if input_type == "Upload Video":
    # File upload section
    uploaded_file = st.file_uploader("Upload a sports video", type=["mp4", "mov", "avi","png"])
    if st.button("Analyze"):
        if uploaded_file is not None and selected_sport:
            # Save the uploaded file
            input_video_path = os.path.join("../data/raw", uploaded_file.name)
            with open(input_video_path, "wb") as f:
                f.write(uploaded_file.read())
            
            st.success(f"Uploaded file: {uploaded_file.name}")
            name = os.path.splitext(uploaded_file.name)[0]
            
            # Process video
            st.info("Processing video. This may take a few minutes...")
            report_path, normal_animation_path, skeleton_animation_path = process_video_pipeline(
                name, input_video_path, selected_sport.lower()
            )
            
            # Display outputs
            st.video(normal_animation_path)
            st.video(skeleton_animation_path)

            # st.markdown("### Analysis Report")
            # with open(report_path, "rb") as pdf_file:
            #     pdf_bytes = pdf_file.read()
            #     pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_bytes.decode("latin1")}" width="100%" height="600"></iframe>'
            #     st.markdown(pdf_display, unsafe_allow_html=True)

            st.download_button(
                "Download Report",
                data=open(report_path, "rb").read(),
                file_name=f"{name}_report.pdf",
                mime="application/pdf",
            )
        else:
            st.error("Please upload a video and select a sport.")

elif input_type == "Webcam":
    # Webcam capture and processing
    if st.button("Start Webcam Analysis"):
        st.info("Initializing webcam...")
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        pose = mp_pose.Pose()
        # Open webcam
        cap = cv2.VideoCapture(0)  # 0 is the default webcam
        if not cap.isOpened():
            st.error("Could not access webcam.")
        else:
            st.success("Webcam is running. Press 'Q' in the webcam window to stop.")
            frame_count = 0
            name = "webcam_capture"
            video_path = f"../data/raw/{name}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to grab frame. Exiting...")
                    break
                
                # Perform marking (e.g., bounding boxes, skeleton)
                marked_frame = frame  # Replace this with your marking function
                out.write(marked_frame)
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
                # cv2.imshow("Webcam Feed - Press 'Q' to Stop", marked_frame)
                frame_count += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()

            st.success("Webcam video captured successfully.")
            st.info("Processing captured video...")
            
            # Process the captured video
            report_path, normal_animation_path, skeleton_animation_path = process_video_pipeline(
                name, video_path, selected_sport.lower()
            )
            
            # Display outputs
            st.video(normal_animation_path)
            st.video(skeleton_animation_path)

            # st.markdown("### Analysis Report")
            # with open(report_path, "rb") as pdf_file:
            #     pdf_bytes = pdf_file.read()
            #     pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_bytes.decode("latin1")}" width="100%" height="600"></iframe>'
            #     st.markdown(pdf_display, unsafe_allow_html=True)

            st.download_button(
                "Download Report",
                data=open(report_path, "rb").read(),
                file_name=f"{name}_report.pdf",
                mime="application/pdf",
            )
