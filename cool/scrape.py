import cv2
import numpy as np
import os
import random
from moviepy.editor import *

def get_image_files(directory):
    supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif','webp']
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    image_files = [f for f in files if any(f.lower().endswith(ext) for ext in supported_formats)]
    return image_files

image_directory = './Memes Folder/'

image_files = get_image_files(image_directory)

if len(image_files) < 10:
    raise ValueError("Not enough images in the directory to choose from.")

combined_image_directory = './Combined Images'
os.makedirs(combined_image_directory, exist_ok=True)

final_video_directory = './Final Videos'
os.makedirs(final_video_directory, exist_ok=True)

audio_directory = './Audio Folder'
audio_files = ['audio1.mp3', 'audio2.mp3', 'audio3.mp3']

for i in range(500):
    # Randomly select two images
    selected_images = random.sample(image_files, 2)
    image1_path = os.path.join(image_directory, selected_images[0])
    image2_path = os.path.join(image_directory, selected_images[1])

    # Read and resize the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    image1 = cv2.resize(image1, (600, 600))
    image2 = cv2.resize(image2, (600, 600))

    # Combine the images vertically
    combined_image = np.vstack((image1, image2))

    # Save the combined image with a unique name
    combined_image_path = os.path.join(combined_image_directory, f'combined_image_{i}.png')
    y=800
    x=1200
    h=1000
    w=600
    crop_img = combined_image[y:y+h, x:x+w]
    cv2.imwrite(combined_image_path, combined_image)
    

    # Create a video clip from the combined image
    image_clip = ImageClip(combined_image_path).set_duration(9.5)
    
    # Randomly select an audio file
    selected_audio = random.choice(audio_files)
    audio_path = os.path.join(audio_directory, selected_audio)
    audio = AudioFileClip(audio_path)

    # Ensure the audio is long enough
    if audio.duration < image_clip.duration:
        raise ValueError("Audio file is shorter than the duration of the image clip.")

    # Set the audio to the image clip
    final_video = image_clip.set_audio(audio.subclip(0, image_clip.duration))

    # Write the final video to a file with a unique name
    final_video_path = os.path.join(final_video_directory, f'final_video_{i}.mp4')
    final_video.write_videofile(final_video_path, fps=1)

    # Delete the original and combined images
    os.remove(image1_path)
    os.remove(image2_path)
    os.remove(combined_image_path)

    # Remove the selected images from the list
    image_files.remove(selected_images[0])
    image_files.remove(selected_images[1])

# Cleanup
cv2.waitKey(0)
cv2.destroyAllWindows()
