import os
import torch
import clip
from PIL import Image

from tests.config import *

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

class_labels = [
    "speed limit 20kmph", 
    "speed limit 30kmph", 
    "speed limit 50kmph", 
    "speed limit 60kmph",
    "speed limit 70kmph",
    "speed limit 80kmph",
    "end of speed limit 80kmph",
    "speed limit 100kmph",
    "speed limit 120kmph",
    "no passing",
    "no passing for vehicles over 3.5 metric tons",
    "right-of-way at the next intersection",
    "priority road",
    "yield",
    "stop",
    "no vehicles",
    "vehicles over 3.5 metric tons prohibited",
    "no entry",
    "general caution",
    "dangerous curve to the left",
    "dangerous curve to the right",
    "double curve",
    "bumpy road",
    "slippery road",
    "road narrows on the right",
    "road work",
    "traffic signals",
    "pedestrians",
    "children crossing",
    "bicycles crossing",
    "beware of ice/snow",
    "wild animals crossing",
    "end of all speed and passing limits",
    "turn right ahead",
    "turn left ahead",
    "ahead only",
    "go straight or right",
    "go straight or left",
    "keep right",
    "keep left",
    "roundabout mandatory",
    "end of no passing",
    "end of no passing by vehicles over 3.5 metric tons"]

# class_labels = ["cat",
#                 "dog",
#                 "horse",
#                 "airplane",
#                 "car",
#                 "truck",
#                 "bird",
#                 "deer",
#                 "frog",
#                 "ship"]


# class_labels = ["stop traffic sign",
#                 "speed limit 30kmph traffic sign",
#                 "speed limit 60kmph traffic sign",
#                 "end of speed limit 80kmph traffic sign",
#                 "childrens crossing traffic sign",
#                 "yield traffic sign"]

# Preprocess the class labels
text = clip.tokenize(class_labels).to(device)

test_class = "wild animals crossing"
output_dict = {}

for img in os.listdir(f"{traffic_train_dataset}/{test_class}"):
    image = preprocess(Image.open(f"{traffic_train_dataset}/{test_class}/{img}")).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Compute the similarity between the image and the class labels
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

    print(f"Image: {img}")

    max_label = ""
    max_prob = 0
    # Print the probabilities for each class label
    probabilities = similarity.cpu().numpy()[0]
    for label, probability in zip(class_labels, probabilities):
        # print(f"{label}: {probability:.4f}")
        if probability > max_prob:
            max_label = label
            max_prob = probability
    if output_dict.get(max_label) is None:
        output_dict[max_label] = 1
    else:
        output_dict[max_label] += 1

    print(f"{max_label}: {max_prob:.4f}")

    print("+"*50)

print(output_dict)
