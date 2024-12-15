# MotionProcessTools
 useful tools for motion data processing, related to SMPL, BVH, FBX, etc.

# SetUP

python==3.11



```bash
pip install -r requirements.txt
```

# Usage


## 1.Kalman_Filter for SMPL joints npy data

if your mocap data is noisy, you can use Kalman_Filter to smooth the data.

<b>notice:</b> the data should be transfor to SMPL joints.

```bash
python ./tools/Kalman_Filter.py
```

## 2. SMPL Joints to BVH
modify the setting in joints2bvh.py, then run the script.
```bash 
python joints2bvh.py
```

based on [animationGPT](https://github.com/fyyakaxyy/animationGPT) for this part.
## 3. BVH to FBX

you need to install blender at first

```bash
Path_to_your_blender -b --python ./tools/bvh2fbx.py -- --BVHF BVH_FOLDER_PATH [--FBXF FBX_FOLDER_PATH]
```

you can use fbx in unity and UE to make animation now :) enjoy it.


# Related
- [animationGPT](https://github.com/fyyakaxyy/animationGPT)
- [AvatarSoul](https://github.com/Gelercatty/AvatarSoul)
