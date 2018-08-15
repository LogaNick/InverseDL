# Can Capsules Estimate Pose?

Deep Learning Inverse Graphics Course Project


## Short Description

Given an image, predict the pose of an object in the image. Data generated in Unity.

## Overview

The goal of this project is to use a capsule network to find the transformation matrices of an object in a scene. Examples and labels are generated using the Unity game engine. A scene is rendering is store as PNG image data that. Scene labels (transformation matrices or a simplified representation) are stored as JSON files. 
    The model is based off of https://github.com/www0wwwjs1/Matrix-Capsules-EM-Tensorflow 


## Quick run instructions

Instructions to run Pose Estimation on Animals dataset

### Environment Setup

Go to the root directory of the repository, and enable environment (refer to environment configurations).

### Go to the correct branch

```
git fetch
git checkout pose_output
```

### Download ```train.tfrecords``` and ```test.tfrecords```
Here’s a link to the folder the data is in: https://drive.google.com/open?id=1Fvg_JfviaiRBOJQ9-fVPRHgwkchJAbQc

Save them in ```./Models/MatrixCapsulesEMTensorflow/data/generated/animals_pose``` folder


### Run on training set

Remove all the previously existing ckpt files
```
rm -rf ./logdir/caps/animals_pose/
```
Open to config.py and set ```is_train``` parameter to ```True``` at line 36
```
vi Models/MatrixCapsulesEMTensorflow/config.py
```
Train the model
```
python train_model.py animals_pose
```

### Run on testing set

Before you run the testing set, you must have several ckpt files exist in ```./logdir```.

Remove all the previously existing ckpt files
```
rm -rf ./test_logdir/caps/animals_pose/
```
Open to config.py and set ```is_train``` parameter to ```False``` at line 36
```
vi Models/MatrixCapsulesEMTensorflow/config.py
```
Test the model
```
python test_model.py animals_pose
```

## Data generation instructions

Data generation is done using the Unity engine version 2018.1.6

To generate data for the animals dataset:
1. Open the Unity project found in “Dataset Generation/Inverse Graphics Dataset Generation”
2. Open the scene “Scenes/Toys No Lighting Rotation”
3. Click on the game object “Swap Toys Before Each Experiment Run”
4. In the inspector, under the “Swap Game Objects Run Experiments” component, change “Save To” to the desired output directory 
5. Click “Run”
6. In the inspector, right click the component “Swap Game Objects Run Experiments” to bring up the context menu
7. In the context menu, click “Run Experiment Runner”
8. Wait until the data is finished generating

## tfrecords generation instructions

The script “data_import/quick_data_load” provides several convenient functions for creating tfrecords based using the generated data. Below is a script to quickly create train/test tfrecords containing ~70% training data and ~30% testing data.

```
from data_import.quick_data_load import *
create_train_test_records("data_import/data/experiment_10/", [0.7, 0.3], False, False, [], ["name", "transformationMatrix"], False, True, [], True)
```
## Packages in Anaconda Environment

(dependencies.txt)
## References

6 x 3D Cute Toy Models, PSIONIC GAMES, Unity Asset Store Asset, https://assetstore.unity.com/packages/3d/characters/6-x-3d-cute-toy-models-105033 Post Processing Stack, Unity Technologies, Unity Asset Store Asset, https://assetstore.unity.com/packages/essentials/post-processing-stack-83912

