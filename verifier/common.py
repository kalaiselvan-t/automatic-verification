# import statements and global variables

import torch
import os
import clip
import inspect
import numpy as np
from PIL import Image
from pyscipopt import Model
from textx import metamodel_from_file


# rival10_labels = ("airplane","car","bird","cat","deer","dog", "frog", "horse", "ship","truck")
rival10_labels = ["stop and give way traffic sign","speed limit 30kmph traffic sign", "speed limit 60kmph traffic sign", "children crossing ahead traffic sign", "end of speed limit 80kmph traffic sign", "pedestrians in road ahead traffic sign", "wild animals traffic sign"]
verification_labels = ["stop and give way traffic sign", "speed limit 30kmph traffic sign", "speed limit 60kmph traffic sign", "children crossing ahead traffic sign", "end of speed limit 80kmph traffic sign", "pedestrians in road ahead traffic sign", "wild animals traffic sign"]

# train_data_path = "/home/kalai/Downloads/RIVAL10/train"
train_data_path = "/home/kalai/Downloads/GTSRB_Final_Training_Images/GTSRB/Final_Training/Images"

class_list = []
image_list = []
network_list = []
rep_list = []

image_focus_regions = {}   # Focus regions of images
class_embeddings = {}      # Image embeddings of classes 
concept_embeddings = {}     # Text embeddings of concepts

# relevant_concepts = {"airplane":["wings","metallic","long","tall"],
#                      "car":["wheels","metallic","rectangular"],
#                      "cat":["ears","eyes","hairy"],
#                      "truck":["wheels","text","metallic","rectangular","long","tall"],
#                      "ship":["metallic","rectangular","wet","long","tall"],
#                      "dog":["long-snout","floppy-ears","ears","hairy"],
#                      "horse":["long-snout","ears","tail","mane","hairy"],
#                      "deer":["long-snout","horns","ears","hairy"],
#                      "frog":["wet"],
#                      "bird":["wings","beak","patterned"]}

# relevant_concepts = {"stop": ["hexagon","stop text"],
#                      "pedestrians": ["circle","pedestrian graphic"],
#                      "animal crossing": ["triangle","animals graphic"],
#                      "road work": ["triangle","road work graphic"],
#                      "keep left": ["circle","downward facing arrow tilted left"],
#                      "keep right": ["circle","downward facing arrow tilted right"],
#                      "speed limit 30kmph": ["circle","number thirty"],
#                      "speed limit 60kmph": ["circle","number sixty"],
#                      "speed limit 80kmph": ["circle","number eighty"],
#                      "end of speed limit 80kmph": ["circle", "number eighty", "striked out graphic"],}

relevant_concepts = {"stop and give way traffic sign": ["octagon shape","word STOP in white letters"],
                     "children crossing ahead traffic sign": ["triangle shape", "two black figures of children"],
                     "pedestrians in road ahead traffic sign": ["circle shape","black figure of a pedestrian walking"],
                     "wild animals traffic sign": ["triangle shape","black figure of a deer leaping"],
                     "road work traffic sign": ["triangle shape","black symbol of a person digging"],
                     "keep left traffic sign": ["circle shape","white arrow pointing to the left"],
                     "keep right traffic sign": ["circle","white arrow pointing to the right"],
                     "speed limit 30kmph traffic sign": ["circle shape","number 30 in black"],
                     "speed limit 60kmph traffic sign": ["circle shape","number 60 in black"],
                     "speed limit 80kmph traffic sign": ["circle shape","number 80 in black"],
                     "end of speed limit 80kmph traffic sign": ["circle shape", "number eighty in black", "diagonal black stripes"],}

# concepts = ["wings","metallic","long","tall","wheels","rectangular","ears","eyes","hairy","text","wet","longsnout","floppyears","tail","mane","beak","patterned","horns","colored-eyes"]
# concepts = ["triangle shape","octagon shape","circle shape","stop text","children graphic","pedestrian graphic","animals graphic","road work graphic","number thirty","number sixty","number eighty","striked out graphic","downward facing arrow tilted left","downward facing arrow tilted right"]
concepts = ["circle shape", "octagon shape", "square shape", "triangle shape", "inverted triangle shape", "word STOP in white letters", "number 30 in black", "number 60 in black", "number 80 in black", "diagonal black stripes", "two black figures of children", "black figure of a pedestrian walking", "black symbol of a deer leaping", "black symbol of a person digging", "white arrow pointing to the left", "white arrow pointing to the right"]