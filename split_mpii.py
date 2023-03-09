#!/usr/bin/env python3.10

# Import the required modules
import numpy as np
import os
import shutil
from scipy.io import loadmat
import sys

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

# first step would be to access the files in the respective images folder
src_path= "mpii_human_pose_v1/images"
path =  "mpii_human_pose_v1"
file_names=os.listdir(src_path)
print(len(file_names))  # there are a total of 24984 images

# now that we have the access to the annotation file, let's proceed further and divide the dataset based on the mpii rules
# where it says, that there are only train and test images in the dataset based on the attribute "img_train"

annot_file = loadmat('mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1')['RELEASE'] 
img_num = len(annot_file['annolist'][0][0][0])

# first lets get the names of the training and testing images
train_data=[]
test_data=[]
for img_id in range(img_num):
    filename = str(annot_file['annolist'][0][0][0][img_id]['image'][0][0][0][0]) #filename
    if (annot_file['img_train'][0][0][0][img_id] == 1):
        if filename in file_names: #It was found out that few filenames in the annotations were absent in the actual image dataset
            train_data.append(filename)
    if (annot_file['img_train'][0][0][0][img_id] == 0):
        if filename in file_names:
            test_data.append(filename)

train_data, valid_data = np.split(train_data, [int(0.7 * len(train_data))])

print("Shape of train data =",len(train_data))      #12655
print("Shape of test data =",len(test_data))        #6908
print("Shape of validation data =",len(valid_data)) #5424


# lets split the datasets considering the filenames
train_dir = os.path.join(path, "train")
test_dir = os.path.join(path, "test")
val_dir = os.path.join(path, "val")
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Move the images into the appropriate directories
for filename in train_data:
    s_path = os.path.join(src_path, filename)
    dst_path = os.path.join(train_dir, filename)
    shutil.copyfile(s_path, dst_path)

for filename in test_data:
    s_path = os.path.join(src_path, filename)
    dst_path = os.path.join(test_dir, filename)
    shutil.copyfile(s_path, dst_path)

for filename in valid_data:
    s_path = os.path.join(src_path, filename)
    dst_path = os.path.join(val_dir, filename)
    shutil.copyfile(s_path, dst_path)