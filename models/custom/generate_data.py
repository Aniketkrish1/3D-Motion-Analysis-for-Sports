import numpy as np
import random
import json

# Function to generate synthetic landmarks data
def generate_synthetic_data(num_samples=1000):
    sports = ["basketball", "yoga", "running", "soccer", "tennis", "cricket", "golf"]
    labels = [
        "bend knees",
        "keep balance",
        "straight posture",
        "low stance",
        "focus on symmetry",
        "avoid overextending",
    ]
    data = []

    for _ in range(num_samples):
        sport = random.choice(sports)
        label = random.choice(labels)

        # Generate synthetic landmarks (25 points, x, y, z)
        landmarks = [
            {"x": np.random.uniform(0.3, 0.7), "y": np.random.uniform(0.4, 0.9), "z": np.random.uniform(0.1, 0.5)}
            for _ in range(25)
        ]
        data.append({"landmarks": landmarks, "sport": sport, "label": label})

    return data

# Generate data and save it as a JSON file
synthetic_data = generate_synthetic_data(2000)
with open("../../data/synthetic_landmarks/landmarks.json", "w") as f:
    json.dump(synthetic_data, f, indent=2)

print("Synthetic data generated and saved as 'synthetic_landmarks.json'.")
