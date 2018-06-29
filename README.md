# InverseDL

Deep Learning Inverse Graphics Project

## Short Description

Given an image, predict the pose of an object in the image. Data generated in Unity.

## Overview

The goal of this project is to use a model (such as a capsule network) to find the transformation matrices of an object in a scene. The scene will be provided as image data that will be generated within the game engine Unity. Labels (transformation matrices or a simplified representation) will also be provided from this data generation. For example, given a scene that consists of a lamp, the model should predict the transformation matrices that describes the lamp’s position, rotation, etc. In the most complicated scenario, the input will be an object O and the output will be the predictions for the **T**ranslation matrix, **R**otation matrix, and **S**cale matrix:

**O** -> model -> **T, R, S**

The project is easily broken up into iterations that can be attempted in order of complexity. An example of the iterations we could follow:

1. Produce 2D images of a single Object that only varies in Translation. Train a model on Translation prediction.
2. Produce 2D images of a single Object that varies in Translation, Rotation, (Scale). Train a model on T,R(,S) prediction.
3. Move to 3D and try steps 1 and/or 2 again
4. Add a second object and repeat steps 1-3
5. Add more objects and repeat 4
6. A task where there are n Objects in a scene. Given Oi, find the pose (T, R, S) of Oi.
7. Record video data, train for trajectories/rotations
8. Determine which objects (or the camera) are moving

This iterative roadmap provides both the opportunity to study something interesting if a single step proves interesting or becomes too difficult, while also giving guidance on how to progress the project if things go well.

## Milestones

1. Produce a general process of generating images of various **T**ranslated, **R**otated, **S**caled **O**bjects. *(June 21 - June 30, ~ 1 week, easy task)*
2. Replicate and Understand the structure of the Capsule NN. *(July 1 - July 4 , ~ 3, 4 days, likely difficult, start while doing task 1)*
3. Reconstruct the Capsule NN code and try several toy tests. *(July 5 - July 15, ~ 10 days)*
4. Revise the code and do various tests. Conclusions. *(July 16 - July 30, ~ 15 days)*


