import bpy
import sys
import os
import argparse
'''
this code based on https://github.com/mcsantiago/bvh2fbx
'''

def bvh2fbx(bvh_folder, fbx_folder):
    bvh_file_list = os.listdir(bvh_folder)
    os.makedirs(fbx_folder, exist_ok=True)
    for bvh_file in bvh_file_list:
        print("bvh_file: ", bvh_file)
        if bvh_file.endswith('.bvh'):
            print(f"Processing {bvh_file}")
            bvh_in = os.path.join(bvh_folder, bvh_file)
            # fbx_out = fbx_folder + bvh_file.split('.')[0] + ".fbx"
            fbx_out = os.path.join(fbx_folder, bvh_file.split('.')[0] + ".fbx")
            # Import the BVH file
            # See https://docs.blender.org/api/current/bpy.ops.import_anim.html?highlight=import_anim#module-bpy.ops.import_anim
            bpy.ops.import_anim.bvh(filepath=bvh_in, filter_glob="*.bvh", global_scale=0.0001, frame_start=1, target='ARMATURE',
                                    use_fps_scale=False, use_cyclic=False, rotate_mode='NATIVE', axis_forward='Z', axis_up='Y')

            # Export as FBX
            # See https://docs.blender.org/api/current/bpy.ops.export_scene.html
            bpy.ops.export_scene.fbx(filepath=fbx_out, axis_forward='Z',
                                    axis_up='Y', use_selection=True, apply_scale_options='FBX_SCALE_NONE')
            print(f"Saved {fbx_out}")
            
            # Clear the scene
            bpy.ops.wm.read_factory_settings(use_empty=True)

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:]
    parser = argparse.ArgumentParser(description='Convert BVH files to FBX format.')
    parser.add_argument('--BVHF', type=str, required=True, help='Path to the folder containing BVH files')
    parser.add_argument('--FBXF', type=str, required=False, default='./FBX', help='Path to the folder to save FBX files')

    print(sys.argv)
    args = parser.parse_args(args)
    print(f"Received BVHF: {args.BVHF}")
    print(f"Received FBXF: {args.FBXF}")
    bvh_folder = args.BVHF
    fbx_folder = args.FBXF
    
    bvh2fbx(bvh_folder, fbx_folder)