from verifier.common import *

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

DEBUG = False
STATUS = False
DIM_SIZE = 512
GAMMA = 0.40