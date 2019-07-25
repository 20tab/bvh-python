# bvh-python
Python module for parsing BVH (Biovision hierarchical data) mocap files

#### Instance Bvh object from .bvh file
```python
>>> from bvh import Bvh
>>> with open('tests/test_freebvh.bvh') as f:
>>>    mocap = Bvh(f.read())
```
 #### Get mocap tree
```python
>>> [str(item) for item in mocap.root]
['HIERARCHY', 'ROOT mixamorig:Hips', 'MOTION', 'Frames: 69', 'Frame Time: 0.0333333']
```
 #### Get ROOT OFFSET
```python
>>> next(mocap.root.filter('ROOT'))['OFFSET']
['0.0000', '0.0000', '0.0000']
```
 #### Get JOINT OFFSET
```python
>>> mocap.joint_offset('mixamorig:Head')
(-0.0, 10.3218, 3.1424)
```
 #### Get Frames
```python
>>> mocap.nframes
69
```
 #### Get Frame Time
```python
>>> mocap.frame_time
0.0333333
```
 #### Get JOINT CHANNELS
```python
>>> mocap.joint_channels('mixamorig:Neck')
['Zrotation', 'Yrotation', 'Xrotation']
```
 #### Get Frame CHANNEL
```python
>>> mocap.frame_joint_channel(22, 'mixamorig:Spine', 'Xrotation')
11.8096
```
 #### Get all JOINT names
```python
>>> mocap.get_joints_names()
['mixamorig:Hips', 'mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2', 'mixamorig:Neck', 'mixamorig:Head', 'mixamorig:HeadTop_End', 'mixamorig:LeftEye', 'mixamorig:RightEye', 'mixamorig:LeftShoulder', 'mixamorig:LeftArm', 'mixamorig:LeftForeArm', 'mixamorig:LeftHand', 'mixamorig:LeftHandMiddle1', 'mixamorig:LeftHandMiddle2', 'mixamorig:LeftHandMiddle3', 'mixamorig:LeftHandThumb1', 'mixamorig:LeftHandThumb2', 'mixamorig:LeftHandThumb3', 'mixamorig:LeftHandIndex1', 'mixamorig:LeftHandIndex2', 'mixamorig:LeftHandIndex3', 'mixamorig:LeftHandRing1', 'mixamorig:LeftHandRing2', 'mixamorig:LeftHandRing3', 'mixamorig:LeftHandPinky1', 'mixamorig:LeftHandPinky2', 'mixamorig:LeftHandPinky3', 'mixamorig:RightShoulder', 'mixamorig:RightArm', 'mixamorig:RightForeArm', 'mixamorig:RightHand', 'mixamorig:RightHandMiddle1', 'mixamorig:RightHandMiddle2', 'mixamorig:RightHandMiddle3', 'mixamorig:RightHandThumb1', 'mixamorig:RightHandThumb2', 'mixamorig:RightHandThumb3', 'mixamorig:RightHandIndex1', 'mixamorig:RightHandIndex2', 'mixamorig:RightHandIndex3', 'mixamorig:RightHandRing1', 'mixamorig:RightHandRing2', 'mixamorig:RightHandRing3', 'mixamorig:RightHandPinky1', 'mixamorig:RightHandPinky2', 'mixamorig:RightHandPinky3', 'mixamorig:RightUpLeg', 'mixamorig:RightLeg', 'mixamorig:RightFoot', 'mixamorig:RightToeBase', 'mixamorig:LeftUpLeg', 'mixamorig:LeftLeg', 'mixamorig:LeftFoot', 'mixamorig:LeftToeBase']
```
 #### Get single JOINT name
```python
>>> mocap.get_joints_names()[17]
'mixamorig:LeftHandThumb2'
```
 #### Get JOINT parent index
```python
>>> mocap.joint_parent_index('mixamorig:Neck')
3
```
 #### Get JOINT parent name
```python
>>> mocap.joint_parent('mixamorig:Head').name
'mixamorig:Neck'
```
 #### Search single item
```python
>>> [str(node) for node in mocap.search('JOINT', 'LeftShoulder')]
['JOINT LeftShoulder']
```
 #### Search all items
```python
>>> [str(node) for node in mocap.search('JOINT')]
['JOINT mixamorig:Spine', 'JOINT mixamorig:Spine1', 'JOINT mixamorig:Spine2', 'JOINT mixamorig:Neck', 'JOINT mixamorig:Head', 'JOINT mixamorig:HeadTop_End', 'JOINT mixamorig:LeftEye', 'JOINT mixamorig:RightEye', 'JOINT mixamorig:LeftShoulder', 'JOINT mixamorig:LeftArm', 'JOINT mixamorig:LeftForeArm', 'JOINT mixamorig:LeftHand', 'JOINT mixamorig:LeftHandMiddle1', 'JOINT mixamorig:LeftHandMiddle2', 'JOINT mixamorig:LeftHandMiddle3', 'JOINT mixamorig:LeftHandThumb1', 'JOINT mixamorig:LeftHandThumb2', 'JOINT mixamorig:LeftHandThumb3', 'JOINT mixamorig:LeftHandIndex1', 'JOINT mixamorig:LeftHandIndex2', 'JOINT mixamorig:LeftHandIndex3', 'JOINT mixamorig:LeftHandRing1', 'JOINT mixamorig:LeftHandRing2', 'JOINT mixamorig:LeftHandRing3', 'JOINT mixamorig:LeftHandPinky1', 'JOINT mixamorig:LeftHandPinky2', 'JOINT mixamorig:LeftHandPinky3', 'JOINT mixamorig:RightShoulder', 'JOINT mixamorig:RightArm', 'JOINT mixamorig:RightForeArm', 'JOINT mixamorig:RightHand', 'JOINT mixamorig:RightHandMiddle1', 'JOINT mixamorig:RightHandMiddle2', 'JOINT mixamorig:RightHandMiddle3', 'JOINT mixamorig:RightHandThumb1', 'JOINT mixamorig:RightHandThumb2', 'JOINT mixamorig:RightHandThumb3', 'JOINT mixamorig:RightHandIndex1', 'JOINT mixamorig:RightHandIndex2', 'JOINT mixamorig:RightHandIndex3', 'JOINT mixamorig:RightHandRing1', 'JOINT mixamorig:RightHandRing2', 'JOINT mixamorig:RightHandRing3', 'JOINT mixamorig:RightHandPinky1', 'JOINT mixamorig:RightHandPinky2', 'JOINT mixamorig:RightHandPinky3', 'JOINT mixamorig:RightUpLeg', 'JOINT mixamorig:RightLeg', 'JOINT mixamorig:RightFoot', 'JOINT mixamorig:RightToeBase', 'JOINT mixamorig:LeftUpLeg', 'JOINT mixamorig:LeftLeg', 'JOINT mixamorig:LeftFoot', 'JOINT mixamorig:LeftToeBase']
```
#### Get joint's direct children
```python
>>> mocap.joint_direct_children('mixamorig:Hips')
[JOINT mixamorig:Spine, JOINT mixamorig:RightUpLeg, JOINT mixamorig:LeftUpLeg]
```
