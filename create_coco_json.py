#!/usr/bin/env python3.10

# Import the required modules
from scipy.io import loadmat
from PIL import Image
import os
import os.path as osp
import numpy as np
import json
import sys


def check_empty(list,name):
    try:
        list[name]
    except ValueError:
        return True

    if len(list[name]) > 0:
        return False
    else:
        return True
    
# unit tests to check the below code functions well
# 1. check if we are in the main folder
try:
    with open("requirements.txt", "r") as f: # if requiremnts file exists in the current folder, then we are in the main folder
        pass
except FileNotFoundError as e:
    print("Please make sure you are in the main folder")
    sys.exit(1)

# 2. check if the images folder exists
try:
    print(len(os.listdir("mpii_human_pose_v1/images")))
except Exception:
    print("Please make sure the Image dataset is downloaded in the main folder")
    sys.exit(1)

# 3. check if the annotation file exists 
try:
    loadmat('mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1')
except Exception:
    print("Please make sure to download the annotation file in the main folder")
    sys.exit(1)

print("Unit test's successful")


db_type = input("Enter the split type for json : Enter train or val or test --> ")
if db_type not in ["test","train","val"]:
    print("Please enter the appropriate input")
    sys.exit(1)

# define the respective folders/paths
img_folder = "mpii_human_pose_v1"
img_dir = os.path.join(img_folder,db_type)
annot_file = loadmat('mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1')['RELEASE']
save_path = img_folder+'/annotations/' + db_type + '.json'

joint_num = 16
fnames = os.listdir(img_dir)
img_num = len(annot_file['annolist'][0][0][0]) # num of images as specified in the annotation file

aid = 0
coco = {'images': [], 'categories': [], 'annotations': []} # annotation file structure for COCO Dataset

for img_id in range(img_num):
    if check_empty(annot_file['annolist'][0][0][0][img_id],'annorect') == False: # if any annotations are present
        filename = str(annot_file['annolist'][0][0][0][img_id]['image'][0][0][0][0]) 
        #print(filename)
        #print(annot_file['act'][0][0][img_id]['act_name'], annot_file['act'][0][0][img_id]['cat_name'],annot_file['act'][0][0][img_id]['act_id']) # ways to access activity details

        if filename in fnames:
            img = Image.open(osp.join(img_dir, filename))
            w,h = img.size
            img_dict = {'id': img_id, 'file_name': filename, 'width': w, 'height': h}
            coco['images'].append(img_dict)

            if db_type == 'test': # test files do not have annotations in them 
                continue
            
            person_num = len(annot_file['annolist'][0][0][0][img_id]['annorect'][0]) #person_num
            joint_annotated = np.zeros((person_num,joint_num)) # person_num* joint_num

            for pid in range(person_num):
                if check_empty(annot_file['annolist'][0][0][0][img_id]['annorect'][0][pid],'annopoints') == False: #kps is annotated
                    bbox = np.zeros((4)) # xmin, ymin, w, h
                    kps = np.zeros((joint_num,3)) # xcoord, ycoord, vis

                    #kps
                    annot_joint_num = len(annot_file['annolist'][0][0][0][img_id]['annorect'][0][pid]['annopoints']['point'][0][0][0])
                    for jid in range(annot_joint_num):
                        annot_jid = annot_file['annolist'][0][0][0][img_id]['annorect'][0][pid]['annopoints']['point'][0][0][0][jid]['id'][0][0]
                        kps[annot_jid][0] = annot_file['annolist'][0][0][0][img_id]['annorect'][0][pid]['annopoints']['point'][0][0][0][jid]['x'][0][0]
                        kps[annot_jid][1] = annot_file['annolist'][0][0][0][img_id]['annorect'][0][pid]['annopoints']['point'][0][0][0][jid]['y'][0][0]
                        kps[annot_jid][2] = 1
                
                    #bbox extract from annotated kps
                    annot_kps = kps[kps[:,2]==1,:].reshape(-1,3)
                    xmin = np.min(annot_kps[:,0])
                    ymin = np.min(annot_kps[:,1])
                    xmax = np.max(annot_kps[:,0])
                    ymax = np.max(annot_kps[:,1])
                    width = xmax - xmin - 1
                    height = ymax - ymin - 1
                    
                    # corrupted bounding box
                    if width <= 0 or height <= 0:
                        continue
                      
                    else:
                        bbox[0] = (xmin + xmax)/2. - width/2
                        bbox[1] = (ymin + ymax)/2. - height/2
                        bbox[2] = width
                        bbox[3] = height


                    person_dict = {'id': aid, 'image_id': img_id, 'category_id': 1, 'area': bbox[2]*bbox[3], 'bbox': bbox.tolist(), 'iscrowd': 0, 'keypoints': kps.reshape(-1).tolist(), 'num_keypoints': int(np.sum(kps[:,2]==1))}
                    coco['annotations'].append(person_dict)
                    aid += 1

category = {
    "supercategory": "person",
    "id": 1,  # as per the COCO standards
    "name": "person",
    "skeleton": [[0,1], # edges connecting 2 jionts
        [1,2], 
        [2,6], 
        [7,12], 
        [12,11], 
        [11,10], 
        [5,4], 
        [4,3], 
        [3,6], 
        [7,13], 
        [13,14], 
        [14,15], 
        [6,7], 
        [7,8], 
        [8,9]] ,
    "keypoints": ["r_ankle", "r_knee","r_hip", 
                    "l_hip", "l_knee", "l_ankle",
                  "pelvis", "throax",
                  "upper_neck", "head_top",
                  "r_wrist", "r_elbow", "r_shoulder",
                  "l_shoulder", "l_elbow", "l_wrist"]}

coco['categories'] = [category]

# To make sure the directory for annotations exist
os.makedirs(img_folder+'/annotations/', exist_ok=True)

# writing the data into a json file
with open(save_path, 'w') as f:
    json.dump(coco, f)
