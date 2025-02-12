import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

# Load JSON file
with open("../data/landmarks/landmarks.json", "r") as file:  # Replace with your file name
    data = json.load(file)

# Parse JSON data
num_frames = len(data)  # Number of frames in the video
num_keypoints = len(data[0])  # Number of keypoints per frame

# Initialize array for keypoints
keypoints = np.zeros((num_frames, num_keypoints, 3))  # (frames, keypoints, [x, y, z])

# Fill the keypoints array with x, y, z data
for i, frame in enumerate(data):
    for j, keypoint in enumerate(frame):
        keypoints[i, j, 0] = keypoint["x"]
        keypoints[i, j, 1] = keypoint["y"]
        keypoints[i, j, 2] = keypoint["z"]

# Default skeletal connections
connections = [
    (0, 1), (1, 2), (2, 3), (3, 7),  # Head and torso
    (0, 4), (4, 5), (5, 6),          # Left arm
    (0, 8), (8, 9), (9, 10),         # Right arm
    (7, 11), (11, 12), (12, 13),     # Left leg
    (7, 14), (14, 15), (15, 16)      # Right leg
]

# Create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the plane background
x = np.linspace(-2, 2, 10)
y = np.linspace(-2, 2, 10)
x, y = np.meshgrid(x, y)
z = np.zeros_like(x)
ax.plot_surface(x, y, z, alpha=0.3, color='gray')

# Add coordinate axes
ax.quiver(0, 0, 0, 1, 0, 0, color='red', label='X-axis')
ax.quiver(0, 0, 0, 0, 1, 0, color='green', label='Y-axis')
ax.quiver(0, 0, 0, 0, 0, 1, color='blue', label='Z-axis')

# Initialize plot elements
points = ax.scatter([], [], [], color='orange', s=50)
lines = [ax.plot([], [], [], color='blue', linewidth=2)[0] for _ in connections]

# Set axis limits
ax.set_xlim(0, 1)  # Adjust based on your data
ax.set_ylim(0, 1)
ax.set_zlim(-0.5, 0.5)

# Set labels
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Human Motion Animation")

# Animation update function
def update(frame):
    points._offsets3d = (
        keypoints[frame, :, 0], 
        keypoints[frame, :, 1], 
        keypoints[frame, :, 2]
    )
    for line, (i, j) in zip(lines, connections):
        x = [keypoints[frame, i, 0], keypoints[frame, j, 0]]
        y = [keypoints[frame, i, 1], keypoints[frame, j, 1]]
        z = [keypoints[frame, i, 2], keypoints[frame, j, 2]]
        line.set_data(x, y)
        line.set_3d_properties(z)
    return points, *lines

# Create animation
ani = FuncAnimation(fig, update, frames=num_frames, interval=50, blit=False)

# Save animation to MP4
ani.save("motion_animation.mp4", writer="ffmpeg", fps=30)

# Show animation
plt.show()
