import numpy as np
import torch
import sys
import os
from .hybrik_loc2rot import HybrIKJointsToRotmat
from Smplify3D.tools.rotation_conversions import matrix_to_axis_angle

import argparse
import joblib
from tqdm import tqdm
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


parser = argparse.ArgumentParser()

parser.add_argument('--dir', type=str, default=None, help="dir for your joints data")
parser.add_argument('--save_folder', type=str, default=None, help="output file name")


opt = parser.parse_args()
print(opt)
hyberik = HybrIKJointsToRotmat()

path = []

fold_item = os.listdir(opt.dir)
for item in fold_item:
    if item.endswith('.npy'):
        path.append(os.path.join(opt.dir, item))

print('begin to process')
if not os.path.isdir(opt.save_folder):
    os.makedirs(opt.save_folder, exist_ok=True)
for p in path:
    
    joints_data = np.load(p)
    
    frame = joints_data.shape[0]
    pose_catch = np.zeros((frame,72))
    trans_catch = np.zeros((frame,3))
    for idx in tqdm(range(frame)):
        joints = joints_data[idx]# frame, 24, 3
        print(joints.shape)
        pose = hyberik(joints)
                # for bvh
        pose_tensor = torch.from_numpy(pose).float()
        pose_axis_angle = matrix_to_axis_angle(pose_tensor)
        # 添加两个空轴角向量（全零向量）
    
        epsilon = 1e-8
        zeros_padding = torch.tensor([[1, 0., 0.],
                                    [1, 0., 0.]], dtype=pose_axis_angle.dtype)
        pose = torch.cat([pose_axis_angle, zeros_padding], dim=0).numpy().reshape(-1)
        
        print(pose.shape)
        pose_catch[idx] = pose
        trans_catch = joints[0, :3]
    
    AISTpp_style_data = {}
    AISTpp_style_data["smpl_pose"] = pose_catch
    AISTpp_style_data["smpl_trans"] = trans_catch
    # (1,)
    AISTpp_style_data["smpl_scaling"] = np.array([1.0])
    
    
    base_filename = os.path.splitext(os.path.basename(p))[0]
    output_filename = f"SMPLPoss_{base_filename}.pkl"
    
    joblib.dump(
        AISTpp_style_data,
        os.path.join(opt.save_folder, output_filename),
        compress=3
    )
    