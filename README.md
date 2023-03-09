# MPII2COCO

This repo aims to convert the MPII format human pose data to COCO JSON format.

This repo includes scripts for the following
1. split the dataset based on "img_train" attribute which specifies if the image belongs to train/test -- > split_mpii.py
2. split the dataset based on ratios for each of the sets -- > split.py
3. create a coco format annotation file for each of the split datasets -- > create_coco_json.py

## Dependencies
1. Python 3.10
2. numpy==1.24.2
3. Pillow==9.4.0
4. scipy==1.10.1

## Folder Structure
![Screenshot from 2023-03-09 12-19-29](https://user-images.githubusercontent.com/95454351/224110190-059c5bc6-af61-4c18-8359-5a468135704d.png)

## Given Task:
Steps-:-
1. Download the dataset from MPII Website MPII Human Pose Database (mpg.de) -- > http://human-pose.mpi-inf.mpg.de/#dataset
2. Write a python script which splits the data into Train, Validation and Test (70,20,10)
3. Generate 3 json files in COCO format for Train , Validation and Test
4. Also make individual folders for image files for each split
5. Upload the code with the folder structure on GitHub and share the link.(Don’t have to upload all the images files to GitHub) 
    
## Thoughts:
1. It was noticed that the MPII Human Pose dataset was majorly designed for a competititon and hence the testset which were supposed to recieve a rich set of annotations were withheld so as to ensure participants don't tune their model on the test set.

2. As a result of which, it was decided that it would be better if we could split based on the design of the dataset, which means all the training data which had annotation were split into train and validation with 70:30 ratio and rest of the non-annotated data was spared for the test set. This way, it is feasible enough to train any model as when we train a model, we require both train and validation set to have annotations.

3. Sideby, keeping in mind that this is a skill-test. I have also made sure to create a script to divide the randomly shuffled data into train-vali-test in the ratio of 70:20:10. But just as we understand, these datasets wouldn't be usable as all the sets contain atleast some percentage of non-annotated files  which doesn't work with the supervised learning.      

4. When it comes to performing data engineering on the data, it is just not enough to split the data, but also to split it in such a way that classes are balanced in eah of the dataset. This is an important fact when it comes to CV but due to the constraint of time it wasn't accomplished.

5. Coming to constructing a json format from MPII format, the code was written keeping in mind about the pose estimation and hence the required attribute which were relevant to the pose were included in the json. But it should also be noted that we coudl eventually more data into json based on the requirement, if it is going to be used by a deep learning model.

## Procedure
1. Download the Image dataset as well as the annotations from the MPII website - http://human-pose.mpi-inf.mpg.de/#dataset
2. Consider the folder structure attached above and place the above files in the right folder (brief description on how the files needs to be placed is provided in the README.md section of each folder).
3. Install all the requirements as per the requirements.txt or by looking into the dependencies
4. Firstly we will start by running the splitter to split the Image dataset into train,test and val using split_mpii.py
6. Secondly, Run create_coco_json.py to generate json files specific to each of the splits
7. Lastly, we can go ahead and get some of the basic statistics of each of the splits using stats.py ( It simply includes statistics sround Image dimensions, Detected People etc. Had a plan to add more statistics and plots based on body points, but couldn't be accomplished due to the constraint of time)

## Future works
1. Implement Dataset splitter based on Class Imbalance improvement.
2. Custom COCO format creator - Get the data requirement from the user and add only those attributes into the JSON.
3. Provided statistical analysis on the occluded points in the image per person
4. Body point Analysis - Points that mostly get occluded in a specific action category. For ex: It is pretty common that knee joint gets occluded when a person is riding a horse etc.
5. Average height of a person in the dataset -- based on the bounding box dimensions.
