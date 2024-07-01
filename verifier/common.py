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
rival10_labels = ["stop", "speed limit 30kmph", "speed_limit_60kmph", "speed limit 80kmph", "end of speed 80kmph", "yield"]
verification_labels = ["stop","speed limit 30kmph","speed limit 60kmph","speed limit 80kmph","end of speed limit 80kmph", "yield"]

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

relevant_concepts = {"stop": ["hexagon","stop text"],
                     "pedestrians": ["circle","pedestrian graphic"],
                     "animal crossing": ["triangle","animals graphic"],
                     "road work": ["triangle","road work graphic"],
                     "keep left": ["circle","downward facing arrow tilted left"],
                     "keep right": ["circle","downward facing arrow tilted right"],
                     "speed limit 30": ["circle","30"],
                     "speed limit 60kmph": ["circle","60"],
                     "speed limit 80": ["circle","80"],
                     "end of speed 80": ["circle", "80", "striked out"],}

# concepts = ["wings","metallic","long","tall","wheels","rectangular","ears","eyes","hairy","text","wet","longsnout","floppyears","tail","mane","beak","patterned","horns","colored-eyes"]
concepts = ["triangle","hexagon","circle","stop text","pedestrian graphic","animals graphic","road work graphic","keep left arrow","keep right arrow","30","60","eighty","striked out","downward facing arrow tilted left","downward facing arrow tilted right"]