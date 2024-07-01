from verifier.common import *
from verifier.config import *

def verification_setup(to_verify = verification_labels):
    get_image_embeddings(to_verify)
    get_class_text_embeddings(to_verify)
    get_concept_text_embeddings(concepts)

def predict_predicate(cls, individual_check=True):
    cls = cls.replace("_"," ")
    if STATUS:
        print(f"Prediction Verification of class: {cls}\n")

    if cls.replace("_"," ") not in image_focus_regions.keys():
        print("cls focus region missing\n")
    else:
        focus_region = image_focus_regions[cls]

        if individual_check:
            # print("Individual Check\n")
            verification_result = []
            for label in verification_labels:
                if label != cls:
                    # print(label)
                    verification_result.append(compare_classes(cls,label,focus_region))
            result = all(verification_result)
        else:
            result = optimize(cls,focus_region)

        if DEBUG:
            if result:
                print("Verification Successful\n")
            else:
                print("Verification Failed\n")
        return result

def compare_classes(cls,other_cls,focus_region):
    if STATUS:
        print(f"Comparing Classes {cls} & {other_cls}\n")
    cls_text_embedding = class_embeddings[cls]
    other_cls_text_embedding = class_embeddings[other_cls]

    result = optimize_predict(cls,focus_region,cls_text_embedding,other_cls_text_embedding)

    if result:
        print("="*30)
        print(f"{cls} > {other_cls}\n")
        print("="*30)
    else:
        print("="*30)
        print(f"{other_cls} > {cls}\n")
        print("="*30)
    
    return result

#===========================================================================================================

def strength_predicate(cls,con_list,individual_check = True):
    cls = cls.replace("_"," ")
    # if STATUS:
    print(f"Strength Verification of concept: {con_list[0]} & {con_list[1]}\n")
    
    if cls not in image_focus_regions.keys():
        print("Class focus region missing\n")
    else:
        focus_region = image_focus_regions[cls]

        if individual_check:
            result = compare_concepts(focus_region,con_list[0],con_list[1])
        else:
            result = optimize(cls,focus_region,con_list)
    
        return result
        

def compare_concepts(focus_region,rel_con,irrel_con):
    if DEBUG:
        print(f"Comparing Concepts {rel_con} & {irrel_con}\n")
    relevant_concept_embedding = concept_embeddings[rel_con.replace("_"," ")]
    irrelevant_concept_embedding = concept_embeddings[irrel_con.replace("_"," ")]

    result = optimize_strength(focus_region,relevant_concept_embedding,irrelevant_concept_embedding)
    
    return result

#===========================================================================================================
# Supporting Functions
#===========================================================================================================
def collect_image_embeddings(image_paths):
    if DEBUG:
        print("Collecting embeddings\n")
    embeddings = []
    for img_path in image_paths:
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)  # Preprocess and add batch dimension
        with torch.no_grad():
            embedding = model.encode_image(image).squeeze().cpu().numpy()
        embeddings.append(embedding)
    embeddings = np.array(embeddings)
    if DEBUG:
        print(f"Returning np.array of shape: {embeddings.shape}\n")
    return embeddings

def get_mean_and_std(embeddings):
    if STATUS:
        print("Calculating mean and std of embeddings\n")
    mean = np.mean(embeddings,axis=0)
    std = np.std(embeddings,axis=0)

    if DEBUG:
        try:
            print(f"Mean(shape): {mean.shape}, std(shape): {std.shape}\n")
        except:
            print(f"Mean: {mean}, std: {std}\n")
    
    return mean,std

def get_focus_region(embeddings,mean,std):
    focus_region = []
    for ind in range(DIM_SIZE):
        lower = mean[ind] - (GAMMA * std[ind])
        upper = mean[ind] + (GAMMA * std[ind])
        focus_region.append([lower,upper])
    
    return focus_region

def get_image_embeddings(labels = rival10_labels):

    # Collect focus regions of all image embeddings
    for label in labels:
        if STATUS:
            print(f"Collecting {label} Image Embeddings\n")
        train_image_paths = [f"{train_data_path}/{label}/{file}" for file in os.listdir(f"{train_data_path}/{label}")]
        img_embeddings = collect_image_embeddings(train_image_paths)
        img_embeddings_mean, img_embeddings_std = get_mean_and_std(img_embeddings)
        focus_region = get_focus_region(img_embeddings,img_embeddings_mean,img_embeddings_std)

        image_focus_regions[label] = focus_region


def collect_text_embeddings(cls):
    captions_template = [f"a bad photo of a {cls} traffic sign",
                                    f"the cartoon {cls} traffic sign",
                                    f"art of the {cls} traffic sign",
                                    f"a drawing of the {cls} traffic sign",
                                    f"a photo of the large {cls} traffic sign",
                                    f"a black and white photo of a {cls} traffic sign",
                                    f"a dark photo of a {cls} traffic sign",
                                    f"a photo of a cool {cls} traffic sign",
                                    f"a photo of a small {cls} traffic sign",
                                    f"a photo containing a {cls} traffic sign",
                                    f"a photo containing the {cls} traffic sign",
                                    f"a photo with a {cls} traffic sign",
                                    f"a photo with the {cls} traffic sign",
                                    f"a photo containing a {cls} sign",
                                    f"a photo containing the {cls} sign",
                                    f"a photo with a {cls} sign",
                                    f"a photo with the {cls} sign",
                                    f"a photo of a {cls} sign",
                                    f"a photo of the {cls} sign"
                                    f"a bad photo of a {cls} traffic sign",
                                    f"a photo of many {cls} traffic sign",
                                    f"a photo of the hard to see {cls} traffic sign",
                                    f"a low resolution photo of the {cls} traffic sign",
                                    f"a rendering of a {cls} traffic sign",
                                    f"a bad photo of the {cls} traffic sign",
                                    f"a cropped photo of the {cls} traffic sign",
                                    f"a photo of a hard to see {cls} traffic sign",
                                    f"a bright photo of a {cls} traffic sign",
                                    f"a photo of a clean {cls} traffic sign",
                                    f"a photo of a dirty {cls} traffic sign",
                                    f"a dark photo of the {cls} traffic sign",
                                    f"a drawing of a {cls} traffic sign",
                                    f"a photo of my {cls} traffic sign" ,
                                    f"a photo of the cool {cls} traffic sign",
                                    f"a close-up photo of a {cls} traffic sign",
                                    f"a black and white photo of the {cls} traffic sign",
                                    f"a painting of the {cls} traffic sign",
                                    f"a painting of a {cls} traffic sign",
                                    f"a pixelated photo of the {cls} traffic sign",
                                    f"a bright photo of the {cls} traffic sign",
                                    f"a cropped photo of a {cls} traffic sign",
                                    f"a photo of the dirty {cls} traffic sign",
                                    f"a jpeg corrupted photo of a {cls} traffic sign",
                                    f"a blurry photo of the {cls} traffic sign",
                                    f"a photo of the {cls} traffic sign",
                                    f"a good photo of the {cls} traffic sign",
                                    f"a rendering of the {cls} traffic sign",
                                    f"a {cls} traffic sign in an image",
                                    f"a photo of one {cls} traffic sign",
                                    f"a doodle of a {cls} traffic sign",
                                    f"a close-up photo of the {cls} traffic sign",
                                    f"a photo of a {cls} traffic sign",
                                    f"the {cls} traffic sign in an image",
                                    f"a sketch of a {cls} traffic sign",
                                    f"a doodle of the {cls} traffic sign",
                                    f"a low resolution photo of a {cls} traffic sign",
                                    f"a photo of the clean {cls} traffic sign",
                                    f"a photo of a large {cls} traffic sign",
                                    f"a photo of a nice {cls} traffic sign",
                                    f"a photo of a weird {cls} traffic sign",
                                    f"a blurry photo of a {cls} traffic sign",
                                    f"a cartoon {cls} traffic sign",
                                    f"art of a {cls} traffic sign",
                                    f"a sketch of the {cls} traffic sign",
                                    f"a pixelated photo of a {cls} traffic sign",
                                    f"a jpeg corrupted photo of the {cls} traffic sign",
                                    f"a good photo of a {cls} traffic sign",
                                    f"a photo of the nice {cls} traffic sign",
                                    f"a photo of the small {cls} traffic sign"]
            
    text_token = clip.tokenize(captions_template).cuda()

    with torch.no_grad():
        text_features = model.encode_text(text_token).squeeze().cpu().numpy()
    
    return text_features

def collect_concept_embeddings(con):
    
    con = f"a road traffic sign with {con}"
    text_token = clip.tokenize([con]).cuda()

    with torch.no_grad():
        text_features = model.encode_text(text_token).squeeze().cpu().numpy()
    
    return text_features

def get_class_text_embeddings(labels=rival10_labels):
    if STATUS:
        print("Collecting all class text embeddings\n")

    for cls in labels:
        embedding = collect_text_embeddings(cls)
        embedding_mean, embedding_std = get_mean_and_std(embedding)

        class_embeddings[cls] = embedding_mean

def get_concept_text_embeddings(concepts):
    if STATUS:
        print("Collecting all concept text embeddings\n")

    for con in concepts:
        embedding = collect_concept_embeddings(con)

        concept_embeddings[con] = embedding

#===========================================================================================================
# Optimization Functions
#===========================================================================================================

def optimize(cls,focus_region, con_list = []):

    model = Model("Predict Verification")

    z = [model.addVar(lb=focus_region[i][0], ub=focus_region[i][1], name=f'z_{i}') for i in range(DIM_SIZE)]

    for i in range(512):
        model.addCons(z[i] >= focus_region[i][0])
        model.addCons(z[i] <= focus_region[i][1])

    for label in verification_labels:
        if label != cls:
            q_class_other = class_embeddings[label]
            q_class = class_embeddings[cls]

            model.addCons(sum(z[i] * (q_class_other[i] / np.linalg.norm(q_class_other)) for i in range(512)) >=
                sum(z[i] * (q_class[i] / np.linalg.norm(q_class)) for i in range(512)))
    
    if con_list:
        # print("Entering loop")
        rel_con_embd = concept_embeddings[con_list[0]]
        irrel_con_embd = concept_embeddings[con_list[1]]
        
        # Add constraints for the concept relation
        model.addCons(sum(z[i] * (irrel_con_embd[i] / np.linalg.norm(irrel_con_embd)) for i in range(512)) >=
                    sum(z[i] * (rel_con_embd[i] / np.linalg.norm(rel_con_embd)) for i in range(512)))

        epsilon = model.addVar(lb=0, name="epsilon")
        # Add a slack variable to maximize the violation strength
        model.addCons(sum(z[i] * (irrel_con_embd[i] / np.linalg.norm(irrel_con_embd)) for i in range(512)) >=
                    epsilon + sum(z[i] * (rel_con_embd[i] / np.linalg.norm(rel_con_embd)) for i in range(512)))
        
        model.setObjective(epsilon, sense='maximize')
            
    model.optimize()

    # model.printStatistics()
    
    # Check the results
    if model.getStatus() == "optimal":
        print("Optimal solution found!")
        if con_list:
            epsilon_opt = model.getVal(epsilon)
            print("Maximized epsilon (strength of violation):", epsilon_opt)
        return False
    else:
        print("No optimal solution found. Status:", model.getStatus())
        return True


def optimize_predict(cls,focus_region,q_class,q_class_other):
    model = Model("Predict Verification")

    z = [model.addVar(lb=focus_region[i][0], ub=focus_region[i][1], name=f'z_{i}') for i in range(DIM_SIZE)]

    for i in range(512):
        model.addCons(z[i] >= focus_region[i][0])
        model.addCons(z[i] <= focus_region[i][1])

  
    model.addCons(sum(z[i] * (q_class_other[i] / np.linalg.norm(q_class_other)) for i in range(512)) >=
        sum(z[i] * (q_class[i] / np.linalg.norm(q_class)) for i in range(512)))
    
    model.optimize()

    # model.printStatistics()

    # Check the results
    if model.getStatus() == "optimal":
        print("Optimal solution found!")
        return False
    else:
        print("No optimal solution found. Status:", model.getStatus())
        return True
    
def optimize_strength(focus_region,rel_con_embd,irrel_con_embd):
    model = Model("Concept Strength verification")

    z = [model.addVar(lb=focus_region[i][0], ub=focus_region[i][1], name=f'z_{i}') for i in range(DIM_SIZE)]

    for i in range(512):
        model.addCons(z[i] >= focus_region[i][0])
        model.addCons(z[i] <= focus_region[i][1])
    
    # Add constraints for the concept relation
    model.addCons(sum(z[i] * (irrel_con_embd[i] / np.linalg.norm(irrel_con_embd)) for i in range(512)) >=
                sum(z[i] * (rel_con_embd[i] / np.linalg.norm(rel_con_embd)) for i in range(512)))

    # Add a slack variable to maximize the violation strength
    epsilon = model.addVar(lb=0, name="epsilon")
    model.addCons(sum(z[i] * (irrel_con_embd[i] / np.linalg.norm(irrel_con_embd)) for i in range(512)) >=
                epsilon + sum(z[i] * (rel_con_embd[i] / np.linalg.norm(rel_con_embd)) for i in range(512)))

    model.setObjective(epsilon, sense='maximize')

    model.optimize()

    # Check the results
    if model.getStatus() == "optimal":
        print("Optimal solution found!")
        epsilon_opt = model.getVal(epsilon)
        print("Maximized epsilon (strength of violation):", epsilon_opt)
        return False
    else:
        print("No optimal solution found. Status:", model.getStatus())
        return True

#=================================================================================================================

