# import statements and global variables

import torch
import os
import clip
import inspect
import numpy as np
from PIL import Image
from pyscipopt import Model
from textx import metamodel_from_file


rival10_labels = ("airplane","car","bird","cat","deer","dog", "frog", "horse", "ship","truck")
verification_labels = ["cat","car","dog","truck","airplane"]

train_data_path = "/home/kalai/Downloads/RIVAL10/train"

class_list = []
image_list = []
network_list = []
rep_list = []

image_focus_regions = {}   # Focus regions of images
class_embeddings = {}      # Image embeddings of classes 
concept_embeddings = {}     # Text embeddings of concepts

relevant_concepts = {"airplane":["wings","metallic","long","tall"],
                     "car":["wheels","metallic","rectangular"],
                     "cat":["ears","eyes","hairy"],
                     "truck":["wheels","text","metallic","rectangular","long","tall"],
                     "ship":["metallic","rectangular","wet","long","tall"],
                     "dog":["long-snout","floppy-ears","ears","hairy"],
                     "horse":["long-snout","ears","tail","mane","hairy"],
                     "deer":["long-snout","horns","ears","hairy"],
                     "frog":["wet"],
                     "bird":["wings","beak","patterned"]}

concepts = ["wings","metallic","long","tall","wheels","rectangular","ears","eyes","hairy","text","wet","longsnout","floppyears","tail","mane","beak","patterned","horns","colored-eyes"]