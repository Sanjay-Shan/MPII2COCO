#!/usr/bin/env python3.10

# Import the required modules
import numpy as np
import os
import shutil
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

# first step would be to access the files in the respective images folder
src_path= "mpii_human_pose_v1/images"
path =  "mpii_human_pose_v1"
file_names=os.listdir(src_path)
print(len(file_names))  # there are a total of 24984 images

# now that we have the access to the files in th image folder, we will proceed to shuffle data --> Split 
np.random.seed(1234)
np.random.shuffle(file_names)

train_data, test_data = np.split(file_names, [int(0.7 * len(file_names))])
valid_data, test_data = np.split(test_data, [int(0.2 * len(file_names))])

print("Shape of train data =",len(train_data))
print(0.7*len(file_names))
print("Shape of test data =",len(test_data))
print(0.1*len(file_names))
print("Shape of validation data =",len(valid_data))
print(0.2*len(file_names))

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