import cv2
import numpy as np
import os
import random
from moviepy.editor import *

def get_image_files(directory):
    supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', 'webp']
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    image_files = [f for f in files if any(f.lower().endswith(ext) for ext in supported_formats)]
    return image_files

# Directories
image_directory = './static/Memes_folder'
combined_image_directory = './static/Combined_Images'
final_video_directory = './static/Final_Videos'
audio_directory = './static/Audio_Folder'
sunset_directory = 'C:/Users/anair/Downloads/cool/Sunset Images/'


# Create directories if they don't exist
os.makedirs(combined_image_directory, exist_ok=True)
os.makedirs(final_video_directory, exist_ok=True)

# Get image and sunset files
image_files = get_image_files(image_directory)
sunset_files = get_image_files(sunset_directory)
audio_files = ['audio1.mp3', 'audio2.mp3']

# Check for sufficient images
if len(image_files) < 1:
    raise ValueError("Not enough images in the directory to choose from.")

for i in range(500):
    # Randomly select an image and a sunset background
    selected_image = random.choice(image_files)
    selected_sunset = random.choice(sunset_files)

    image1_path = os.path.join(image_directory, selected_image)
    sunset_image_path = os.path.join(sunset_directory, selected_sunset)

    # Read and resize the images
    image1 = cv2.imread(image1_path)
    sunset_image = cv2.imread(sunset_image_path)

    # Get sunset image dimensions
    sunset_height, sunset_width, _ = sunset_image.shape
    
    # Desired aspect ratio
    target_aspect_ratio = 9 / 16
    
    # Determine the new dimensions and crop area based on aspect ratio
    if sunset_width / sunset_height > target_aspect_ratio:
        # Sunset image is wider than the target ratio, crop width
        new_width = int(sunset_height * target_aspect_ratio)
        crop_x = (sunset_width - new_width) // 2
        cropped_sunset_image = sunset_image[:, crop_x:crop_x + new_width]
    else:
        # Sunset image is taller than the target ratio, crop height
        new_height = int(sunset_width / target_aspect_ratio)
        crop_y = (sunset_height - new_height) // 2
        cropped_sunset_image = sunset_image[crop_y:crop_y + new_height, :]

    # Resize the cropped sunset image to the target size
    target_height = 1080
    target_width = int(target_height * target_aspect_ratio)
    cropped_sunset_image = cv2.resize(cropped_sunset_image, (target_width, target_height))

    # Resize the meme image to a smaller size and center it on the sunset background
    meme_height, meme_width = 500, 500
    image1 = cv2.resize(image1, (meme_width, meme_height))

    # Calculate the center position
    y_offset = (cropped_sunset_image.shape[0] - image1.shape[0]) // 2
    x_offset = (cropped_sunset_image.shape[1] - image1.shape[1]) // 2

    # Place the meme image on the cropped sunset background
    combined_image = cropped_sunset_image.copy()
    combined_image[y_offset:y_offset+meme_height, x_offset:x_offset+meme_width] = image1

    # Save the combined image
    combined_image_path = os.path.join(combined_image_directory, f'combined_image_{i}.png')
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
    final_video_path = os.path.join(final_video_directory, f'Like and Subscribe if u want to revisit this! #memes #funnyshorts #funny #shorts#shortstrend#jokes{i}.mp4')
    final_video.write_videofile(final_video_path, fps=24)

    # Clean up
    os.remove(combined_image_path)
    image_files.remove(selected_image)

# Cleanup OpenCV
cv2.waitKey(0)
cv2.destroyAllWindows()
