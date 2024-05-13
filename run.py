from selenium import webdriver
from flask import Flask, redirect
import re
from collections import OrderedDict
import time

# Define the maximum cache size and duration in seconds (4 hours)
MAX_CACHE_SIZE = 50
CACHE_DURATION = 4 * 60 * 60  # 4 hours in seconds
cache = OrderedDict(maxlen=MAX_CACHE_SIZE)

# Validate query, modify this regex as needed
VALID_QUERY_REGEX = re.compile(r'^[\w\-\.\/]+$') 

app = Flask(__name__)

def invalidate_old_entries():
    current_time = time.time()
    one_hour_ago = current_time - 3600  # 1 hour in seconds

    # Iterate over a copy of the keys to avoid modifying while iterating
    for key in list(cache.keys()):
        timestamp, _ = cache[key]
        if timestamp < one_hour_ago:
            del cache[key]

# Define the base URL for scraping
base_url = "https://instagram.com"  # Replace with your actual base URL

# Initialize WebDriver globally
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')
options.add_argument(f'user-agent={user_agent}')
browser = webdriver.Chrome(options=options) 

# Function to handle web scraping using Selenium
def get_video_source(query_string):
    try:
        browser.delete_all_cookies()
        query_string = "/" + query_string
        url = f"{base_url}{query_string}"  # Combine base URL and video ID
        browser.get(url)

        # Replace sleep with explicit wait if possible
        browser.implicitly_wait(10)

        browser.save_screenshot('ss_ig_reel.png')

        # Locate the video element using your specific xpath
        try:
            # Reels
            video_element = browser.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div/div/div/div/video"
            )
        except:
            # Post (image)
            video_element = browser.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]/div/div/div/div/div/div/div[1]/img"
            )

        # Get the video source and return it
        video_source = video_element.get_attribute("src")
        return video_source

    except Exception as e:
        # Handle exceptions and return a default URL or re-raise the exception
        print("Error: ")
        print(e)
        browser.get("https://api.dev.gabrielkheisa.xyz/")
        return base_url


@app.route("/", methods=["GET"])  # Route for empty query string
def handle_empty_query():
    return redirect("https://github.com/gabrielkheisa/instagram-downloader")

@app.route("/<path:query_string>", methods=["GET"])
def get_video_source_server(query_string):
    global cache  # Ensure we reference the global cache variable
    print(query_string)
    if len(query_string) > 80:
        return '', 204

    if not VALID_QUERY_REGEX.match(query_string):
        return "Invalid link", 400


    # Clean up entries older than 4 hours
    current_time = time.time()
    keys_to_remove = []
    for key in list(cache.keys()):
        value = cache[key]
        if isinstance(value, dict) and "timestamp" in value:
            timestamp = value["timestamp"]
            if current_time - timestamp >= CACHE_DURATION:
                keys_to_remove.append(key)

    for key in keys_to_remove:
        cache.pop(key, None)

    if query_string in cache:
        # Move the existing entry to the front of the cache and update its timestamp
        video_source = cache.pop(query_string)
        video_source["timestamp"] = time.time()
        cache[query_string] = video_source
        return redirect(video_source["url"])

    # Get the video source sequentially
    video_source = get_video_source(query_string)

    # Add the new entry to the cache with a timestamp
    cache[query_string] = {"url": video_source, "timestamp": time.time()}

    return redirect(video_source)

if __name__ == "__main__":
    app.run(debug=False, port=8080, host="0.0.0.0")
