import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

# Point-based 3D animation
def create_3d_animation(landmarks_path, output_file):
    with open(landmarks_path, "r") as f:
        data = json.load(f)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    def update(frame_num):
        ax.clear()
        frame_landmarks = data[frame_num]
        x = [lm["x"] for lm in frame_landmarks]
        y = [lm["y"] for lm in frame_landmarks]
        z = [lm["z"] for lm in frame_landmarks]

        ax.scatter(x, y, z, c="blue", marker="o")
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])

        # Rotate the view
        angle = frame_num * 2  # Adjust rotation speed
        ax.view_init(elev=-120, azim=270)
        ax.axis("off")

    anim = FuncAnimation(fig, update, frames=len(data), interval=50)
    anim.save(output_file, writer="ffmpeg", fps=20)

# Skeleton-based 3D animation
def create_skeleton_3d_animation(landmarks_path, output_file):
    with open(landmarks_path, "r") as f:
        data = json.load(f)

    skeleton_connections = [
        (11, 12), (12, 14), (14, 16),  # Right arm
        (11, 13), (13, 15),           # Left arm
        (23, 24), (24, 26), (26, 28), # Right leg
        (23, 25), (25, 27),           # Left leg
        (11, 23), (12, 24)            # Torso
    ]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    def update(frame_num):
        ax.clear()
        frame_landmarks = data[frame_num]
        x = [lm["x"] for lm in frame_landmarks]
        y = [lm["y"] for lm in frame_landmarks]
        z = [lm["z"] for lm in frame_landmarks]
        
        for start, end in skeleton_connections:
            ax.plot(
                [x[start], x[end]], [y[start], y[end]], [z[start], z[end]],
                c="red"
            )
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])
        ax.view_init(elev=130, azim=90)
        ax.axis("off")
    anim = FuncAnimation(fig, update, frames=len(data), interval=50)
    anim.save(output_file, writer="ffmpeg", fps=20)



# create_3d_animation("../data/landmarks/landmarks.json", "../outputs/animations/sample1.mp4")
# create_skeleton_3d_animation("../data/landmarks/landmarks.json", "../outputs/animations/sample2.mp4")


# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import json
# import numpy as np

# # Function to create a 3D animation with points marked on the human body
# def create_annotated_video(landmarks_path, output_path):
#     with open(landmarks_path, "r") as f:
#         data = json.load(f)

#     # Extract landmarks
#     frames = len(data)
#     keypoints = np.array([
#         [[lm["x"], lm["y"], lm["z"]] for lm in frame] 
#         for frame in data
#     ])

#     # Create a figure for the animation
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")

#     def update(frame):
#         ax.clear()
#         ax.set_xlim(0, 1)  # Normalize coordinates to a [0, 1] range
#         ax.set_ylim(0, 1)
#         ax.set_zlim(-1, 1)  # Z-coordinates might have negative values

#         # Plot the points for this frame
#         points = keypoints[frame]
#         xs, ys, zs = points[:, 0], points[:, 1], points[:, 2]
#         ax.scatter(xs, ys, zs, color="blue", label="Body Points")

#         ax.set_title(f"Frame: {frame + 1}/{frames}")

#     ani = FuncAnimation(fig, update, frames=frames, interval=50)
#     ani.save(output_path, writer="ffmpeg", fps=20)
#     plt.close(fig)

def create_skeleton_animation(landmarks_path, output_file):
    with open(landmarks_path, "r") as f:
        data = json.load(f)

    # Skeleton connections (start -> end indices)
    skeleton_connections = [
        (11, 12), (12, 14), (14, 16),  # Right arm
        (11, 13), (13, 15),           # Left arm
        (23, 24), (24, 26), (26, 28), # Right leg
        (23, 25), (25, 27),           # Left leg
        (11, 23), (12, 24)            # Torso
    ]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    def update(frame_num):
        ax.clear()

        frame_landmarks = data[frame_num]
        x = [lm["x"] for lm in frame_landmarks]
        y = [lm["y"] for lm in frame_landmarks]
        z = [lm["z"] for lm in frame_landmarks]

        # Adjust axis labels
        ax.set_xlabel("X (Horizontal)")
        ax.set_ylabel("Y (Height)")
        ax.set_zlabel("Z (Depth)")

        # Draw connections
        for start, end in skeleton_connections:
            ax.plot(
                [x[start], x[end]], [y[start], y[end]], [z[start], z[end]],
                c="blue", linewidth=2
            )
        
        # Mark joints
        ax.scatter(x, y, z, c="red", s=20)  # Joints in red

        # Set consistent axis limits
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])

        # Set the viewing angle
        ax.view_init(elev=-120, azim=270)
        ax.axis("off")
    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(data), interval=50)
    anim.save(output_file, writer="ffmpeg", fps=20)
    plt.close(fig)

# # Example usage
# # create_skeleton_3d_animation("path_to_landmarks.json", "skeleton_animation.mp4")

# create_skeleton_animation("../data/landmarks/landmarks.json", "../outputs/annotated_videos/annotated_video3.mp4")