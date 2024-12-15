import numpy as np
import os
from filterpy.kalman import KalmanFilter

def Kalman_Filter(folder_path, save_path):
    for filename in os.listdir(folder_path):
        if not filename.endswith('.npy'):
            continue
        # 加载数据
        npy_file_path = os.path.join(folder_path, filename)
        positions = np.load(npy_file_path)

        if positions.shape[0] < 2:
            continue
        if positions.shape[1] != 22:
            positions = positions[:, :-30, :]
        num_frames, num_joints, _ = positions.shape
        state_dim_per_joint = 3

        kfs = [KalmanFilter(dim_x=state_dim_per_joint, dim_z=state_dim_per_joint) for _ in range(num_joints)]
        for joint_id, kf in enumerate(kfs):
            kf.x = positions[0][joint_id]
            kf.P *= 1e-4
            kf.F = np.eye(state_dim_per_joint)
            kf.H = np.eye(state_dim_per_joint)
            kf.Q *= 1e-1
            kf.R *= 0.4

        filtered_positions = np.zeros_like(positions)
        for frame in range(num_frames):
            observed_data = positions[frame]
            for joint_id, kf in enumerate(kfs):
                kf.predict()
                kf.update(observed_data[joint_id])
                filtered_positions[frame][joint_id] = kf.x

        output_file_path = os.path.join(save_path, filename)
        np.save(output_file_path, filtered_positions)
        print(f"Processed and saved: {output_file_path}")

if __name__ == '__main__':
    folder_path = './taichi3'
    save_path = './taichi3_filtered'

    os.makedirs(save_path, exist_ok=True)
    Kalman_Filter(folder_path, save_path)
