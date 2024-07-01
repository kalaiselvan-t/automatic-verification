import os
import torch
import clip
from PIL import Image

from tests.config import *

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

class_labels = [
    "speed limit 20kmph traffic sign", 
    "speed limit 30kmph traffic sign", 
    "speed limit 50kmph traffic sign", 
    "speed limit 60kmph traffic sign",
    "speed limit 70kmph traffic sign",
    "speed limit 80kmph traffic sign",
    "end of speed limit 80kmph traffic sign",
    "speed limit 100kmph traffic sign",
    "speed limit 120kmph traffic sign",
    "no passing traffic sign",
    "no passing for vehicles over 3.5 metric tons traffic sign",
    "right-of-way at the next intersection traffic sign",
    "priority road traffic sign",
    "german yield traffic sign",
    "stop traffic sign",
    "no vehicles traffic sign",
    "vehicles over 3.5 metric tons prohibited traffic sign",
    "no entry traffic sign",
    "general caution traffic sign",
    "dangerous curve to the left traffic sign",
    "dangerous curve to the right traffic sign",
    "double curve traffic sign",
    "bumpy road traffic sign",
    "slippery road traffic sign",
    "road narrows on the right traffic sign",
    "road work traffic sign",
    "traffic signals traffic sign",
    "pedestrians traffic sign",
    "children crossing traffic sign",
    "bicycles crossing traffic sign",
    "beware of ice or snow traffic sign",
    "wild animals crossing traffic sign",
    "end of all speed and passing limits traffic sign",
    "turn right ahead traffic sign",
    "turn left ahead traffic sign",
    "ahead only traffic sign",
    "go straight or right sign",
    "go straight or left sign",
    "keep right traffic sign",
    "keep left traffic sign",
    "roundabout mandatory traffic sign",
    "end of no passing traffic sign",
    "end of no passing by vehicles over 3.5 metric tons traffic sign"]

# class_labels = ["road work traffic sign",
#                 "stop traffic sign",
#                 "speed limit 100kmph traffic sign",
#                 "pedestrian traffic sign",
#                 "speed limit 50kmph traffic sign",
#                 "speed limit 20kmph traffic sign"]

# Preprocess the class labels
test_labels = "no passing"
correct_label = "no passing traffic sign"
test_folder = f"{test_data_set}/{test_labels}"

text = clip.tokenize(class_labels).to(device)

correct_classifications = 0

# print(len(os.listdir(test_folder)))

for img in os.listdir(test_folder):
    # print(img)

    if not img.endswith(".ppm"):
        continue
    image = preprocess(Image.open(f"{test_folder}/{img}")).unsqueeze(0).to(device)
    # print("img collected")

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Compute the similarity between the image and the class labels
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    # print(f"Image: {img}")

    # Print the probabilities for each class label
    probabilities = similarity.cpu().numpy()[0]
    max_prob = 0
    max_label = ""

    for label, probability in zip(class_labels, probabilities):
        if probability > max_prob:
            max_prob = probability
            max_label = label

    if max_label == correct_label:
        correct_classifications += 1

    print(f"{max_label}: {max_prob:.4f}")

print(f"Accuracy: {correct_classifications}/{len(os.listdir(test_folder))}")
print("+"*50)
