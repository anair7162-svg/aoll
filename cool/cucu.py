from flask import Flask, render_template, request, redirect, url_for
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from flask import jsonify
import cv2
import numpy as np
import random
from moviepy.editor import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_images():
    search_query = request.form['search_query']
    num_images = int(request.form['num_images'])

    # Set up Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Directory to save images
    image_directory = './static/memes_folder'
    os.makedirs(image_directory, exist_ok=True)

    # Google Images search URL
    search_url = "https://www.google.com/imghp?hl=en"

    # Perform Google Images search
    driver.get(search_url)
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Scroll down to load more images
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get image URLs
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    images = soup.find_all('img')

    # Download images
    downloaded_count = 0
    for idx, img in enumerate(images):
        if downloaded_count >= num_images:
            break
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            try:
                img_data = requests.get(img_url).content
                img_file = BytesIO(img_data)
                image = Image.open(img_file)
                width, height = image.size
                if width >= 20 and height >= 20:
                    img_path = os.path.join(image_directory, f'image{downloaded_count + 1}.jpg')
                    with open(img_path, 'wb') as handler:
                        handler.write(img_data)
                    downloaded_count += 1
            except Exception as e:
                print(f"Skipping image {idx + 1}: {e}")

    driver.quit()
    return jsonify(message="Images successfully downloaded!")
    return redirect(url_for('index'))

@app.route('/create_videos', methods=['POST'])
def create_videos():
    def get_image_files(directory):
        supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        image_files = [f for f in files if any(f.lower().endswith(ext) for ext in supported_formats)]
        return image_files

    image_directory = './static/Memes_folder'
    combined_image_directory = './static/Combined_Images'
    final_video_directory = './static/Final_Videos'
    audio_directory = './static/Audio_Folder'
    
    os.makedirs(combined_image_directory, exist_ok=True)
    os.makedirs(final_video_directory, exist_ok=True)+

    image_files = get_image_files(image_directory)

    if len(image_files) < 10:
        return "Not enough images in the directory to choose from."

    audio_files = ['audio1.mp3', 'audio2.mp3']

    for i in range(10):  # Reduced to 10 for demonstration purposes
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
        cv2.imwrite(combined_image_path, combined_image)

        # Create a video clip from the combined image
        image_clip = ImageClip(combined_image_path).set_duration(9.5)
        
        # Randomly select an audio file
        selected_audio = random.choice(audio_files)
        audio_path = os.path.join(audio_directory, selected_audio)
        audio = AudioFileClip(audio_path)

        # Ensure the audio is long enough
        if audio.duration < image_clip.duration:
            continue  # Skip this iteration

        # Set the audio to the image clip
        final_video = image_clip.set_audio(audio.subclip(0, image_clip.duration))

        # Write the final video to a file with a unique name
        final_video_path = os.path.join(final_video_directory, f'Like and Subscribe if u want to revisit this! #memes #funnyshorts #funny #shorts#shortstrend#jokes{i}.mp4')
        final_video.write_videofile(final_video_path, fps=1)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
