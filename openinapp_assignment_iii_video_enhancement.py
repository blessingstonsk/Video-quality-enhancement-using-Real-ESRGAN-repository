# -*- coding: utf-8 -*-
"""Openinapp Assignment III-Video Enhancement

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s0_2trebiowij27uIZQWFtcu-NoMlgge

# **Assignment 3:**
Showcase your proficiency in developing an advanced AI model capable of enhancing the quality of a video by upscaling its resolution and reducing noise. And only use the videos provided in the PDF to work on the upscaling task.

# **Step 1: Download required libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive, files
import os, shutil, subprocess
drive_mounted = False
temp_folder = 'tmp_frames'
result_folder = 'results'
!git clone https://github.com/xinntao/Real-ESRGAN.git
# %cd Real-ESRGAN
# Set up the environment
!pip install basicsr facexlib gfpgan
!pip install -r requirements.txt
!python setup.py develop
# Download the pre-trained model
!wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P experiments/pretrained_models
# %cd ..

"""# **Step 2: Upload the video file:**"""

if drive_mounted is not True:

  upload_folder = 'upload'

  if os.path.isdir(upload_folder):
      shutil.rmtree(upload_folder)

  os.mkdir(upload_folder)

  # upload images
  uploaded = files.upload()
  file_name = next(iter(uploaded))
  input_path = f'/content/{upload_folder}/{file_name}'
  for filename in uploaded.keys():
    dst_path = os.path.join(upload_folder, filename)
    print(f'move {filename} to {dst_path}')
    shutil.move(filename, dst_path)
else:
  print("drive mounted nothing to do here move along")

"""# **Step 3: Extract the frames from the video file:**"""

if os.path.isdir(temp_folder):
  shutil.rmtree(temp_folder)

os.mkdir(temp_folder)
print(f'Extracting Frames to: {temp_folder}')
cmd = [
       'ffmpeg',
       '-i',
       input_path,
       '-qscale:v',
       '1',
       '-qmin',
       '1',
       '-qmax',
       '1',
       '-vsync',
       '0',
       f'{temp_folder}/frame_%08d.png'
]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print(stderr)
    raise RuntimeError(stderr)
else:
    frame_count = len(os.listdir(f'/content/{temp_folder}'))
    print(f"Done, Extracted {frame_count} Frames")

"""# **Step 4: Run ERSGAN on Extracted Frames!**"""

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/Real-ESRGAN
frame_count = len(os.listdir(f'/content/{temp_folder}'))
print(f"Enhancing {frame_count} Frames with ESRGAN...")
cmd = [
    'python',
    'inference_realesrgan.py',
    '-n',
    'RealESRGAN_x4plus',
    '-i',
    f'../{temp_folder}',
    '--outscale',
    '4',
    '--face_enhance'
]
#process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# stdout, stderr = process.communicate()
# if process.returncode != 0:
#     print(stderr)
#     raise RuntimeError(stderr)
# else:
#     print("Done Extracting Frames")
!{' '.join(cmd)}
print("Done Enhancing Frames")
# %cd ..

"""# **Step 4: Create the same video from the enhanced frames**"""

import subprocess
frame_count = len(os.listdir(f'/content/{temp_folder}'))
if os.path.isdir(result_folder):
  shutil.rmtree(result_folder)
os.mkdir(result_folder)

fps = 15
print(f"Recompiling {frame_count} Frames into Video...")
cmd = [
       'ffmpeg',
       '-i',
       f'/content/Real-ESRGAN/results/frame_%08d_out.png',
       '-c:a',
       'copy',
       '-c:v',
       'libx264',
       '-r',
       str(fps),
       '-pix_fmt',
       'yuv420p',
       f'{result_folder}/enhanced_{file_name}'
]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print(stderr)
    raise RuntimeError(stderr)
else:
    print("Done Recreating Video")

"""# **Final result is saved in the path: /content/Real-ESRGAN/results**"""