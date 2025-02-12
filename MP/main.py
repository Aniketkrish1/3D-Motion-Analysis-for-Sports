from preprocess import preprocess_video
from analysis import extract_landmarks, analyze_sport , landmarks , analyze_posture
from visualization import  create_skeleton_3d_animation,create_skeleton_animation
from report import generate_report
from recommendation import recommend
import os

def process_video_pipeline(name , input_video_path, sport):
    # Define paths
    preprocessed_video_path = f"../data/processed/{name}.mp4"
    landmarks_path = f"../data/landmarks/{name}.json"
    landmark_analysis_path=f"../data/landmark_analysis/{name}.json"
    normal_animation_path = f"../outputs/annotated_videos/{name}.mp4"
    skeleton_animation_path = f"../outputs/animations/{name}.mp4"
    report_path = f"../outputs/reports/{name}.pdf"
    
    # Create directories
    # os.makedirs("data/processed", exist_ok=True)
    # os.makedirs("data/landmarks", exist_ok=True)

    # Pipeline
    preprocess_video(input_video_path, preprocessed_video_path)
    extract_landmarks(preprocessed_video_path, landmarks_path)
    landmarks(preprocessed_video_path,landmark_analysis_path)
    normal_stats= analyze_posture(landmark_analysis_path, sport)
    create_skeleton_3d_animation(landmarks_path, normal_animation_path)
    create_skeleton_animation(landmarks_path,skeleton_animation_path)
    recommendations=recommend(landmark_analysis_path,sport)
    generate_report(
        sport,
        landmarks_path,
        normal_stats,
        recommendations,
        normal_animation_path,
        skeleton_animation_path,
        report_path,
    )

    return report_path, normal_animation_path, skeleton_animation_path
