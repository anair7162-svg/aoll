import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Directory to save images
image_directory = './Memes Folder'
os.makedirs(image_directory, exist_ok=True)

# Google Images search URL
search_url = "https://www.google.com/imghp?hl=en"

# Perform Google Images search
driver.get(search_url)
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('school memes')
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
for idx, img in enumerate(images):
    img_url = img.get('src')
    if img_url and img_url.startswith('http'):
        img_data = requests.get(img_url).content
        img_path = os.path.join(image_directory, f'image{idx + 1}.jpg')
        with open(img_path, 'wb') as handler:
            handler.write(img_data)

driver.quit()
print(f"Downloaded {len(images)} images to {image_directory}")
