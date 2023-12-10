from selenium import webdriver
from flask import Flask, request, redirect
import concurrent.futures
from collections import OrderedDict

app = Flask(__name__)

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
browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options) 

cache = OrderedDict(maxlen=50)

# Function to handle web scraping using Selenium
def get_video_source(query_string):
    try:
        browser.delete_all_cookies()

        query_string = "/" + query_string
        url = f"{base_url}{query_string}"  # Combine base URL and video ID
        browser.get(url)

        # Replace sleep with explicit wait if possible
        browser.implicitly_wait(4)

        # Locate the video element using your specific xpath
        video_element = browser.find_element_by_xpath(
            "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[1]/div/article/div/div[1]/div/div/div/div/div/div/div/video"
        )

        # Get the video source and return it
        video_source = video_element.get_attribute("src")
        return video_source

    except Exception as e:
        # Handle exceptions and return a default URL or re-raise the exception
        return base_url

@app.route("/<path:query_string>", methods=["GET"])
def get_video_source_server(query_string):
    if len(query_string) > 30:
        # Reject the request by returning a 414 error code
        return abort(414, description="Query string too long")
    if query_string in cache:
        # If cached, move to the front of the OrderedDict to update its age
        video_source = cache.pop(query_string)
        cache[query_string] = video_source
        return redirect(video_source)
    # Create a ThreadPoolExecutor for parallel execution with a timeout of 3 seconds
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_video_source, query_string)
        try:
            video_source = future.result(timeout=10)  # Timeout set to 3 seconds
            cache[query_string] = video_source
            return redirect(video_source)
        except concurrent.futures.TimeoutError:
            # Handle timeout - return a default URL or handle as needed
            return redirect(base_url)

if __name__ == "__main__":
    app.run(debug=False, port=8080, host="0.0.0.0")