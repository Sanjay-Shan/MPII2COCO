# Import the required modules
import json
import statistics as stat
from collections import defaultdict
import numpy as np
import sys

db_type = input("Enter the split type to generate the stats : test or train or val -->")
if db_type not in ["test","train","val"]:
    print("Please enter the appropriate input")
    sys.exit(1)

path= "mpii_human_pose_v1/annotations/"+db_type+".json"

try:
    with open(path, "r") as f:
        data =json.load(f)
except Exception:
    print("Please check if you have a json file in the given path : mpii_human_pose_v1/annotations/")
    sys.exit(1)

width=[]
height=[]
dims=[]
for i in data['images']:
    width.append(i['width'])
    height.append(i['height'])
    dims.append(i['width']*i['height'])

dim_mode = dims.index(stat.mode(dims))
print("Most common Image dimension :",width[dim_mode],height[dim_mode])

# lets get the max image dimensions in the dataset
dim_max = dims.index(max(dims))
print("Largest Image Dimension :",width[dim_max],height[dim_max])

# lets get the min image dimensions in the dataset
dim_min = dims.index(min(dims))
print("Smallest Image Dimension :",width[dim_min],height[dim_min])

# lets look into the annotations
# lets try to get average number of persons in an image
try:
    data['annotations'][0]
except Exception as e:
    print("This is a test set and hence annotation may not exist")
    sys.exit(1)

person=defaultdict(int)
for i in data['annotations']:
    person[i["image_id"]]+=1

max_pcount=sorted(person.items(), key=lambda x:x[1])[-1][1]
min_pcount=sorted(person.items(), key=lambda x:x[1])[0][1]
total_pcount=sum(person.values())

print("Max people detected in an Image :",max_pcount)
print("Min people detected in an Image :",min_pcount)
print("Total number of people in this dataset",total_pcount)
 