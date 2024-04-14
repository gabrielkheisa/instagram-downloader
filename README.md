# Instagram Video Downloader

This micro web server allows you to download Instagram Reels videos by providing their query parameters. It utilizes Selenium to control a Chromium browser instance and navigate to the Instagram webpage. Once the video is loaded, it extracts the CDN link and redirects you to it. 

### Usage:
```
https://ig.gabrielkheisa.xyz/<query_params_from_instagram.com>
```
### Example:
**Source**
```
https://www.instagram.com/reel/Cz3dNmDMVC9/?igshid=MzRlODBiNWFlZA==
```
**Replace**
```
https://ig.gabrielkheisa.xyz/reel/Cz3dNmDMVC9/?igshid=MzRlODBiNWFlZA==
```
### Returns redirect:
```
https://scontent.cdninstagram.com/v/t66.30100-16/316926421_1723935788092224_3596729375098306652_n.mp4?_nc_ht=scontent.cdninstagram.com&_nc_cat=100&_nc_ohc=6lyBPVcj...............
```
Notes: This redirect URL (https://scontent.cdninstagram.com/...) has expiration, in which you need to re-run the query to get a new URL signature

## DISCLAIMER:

This micro web server does not directly download the Instagram Reels video. It simply locates the Instagram CDN link for the video and redirects you to it. Therefore, it is not technically a "downloader" but rather a **CDN link extractor and redirector**.

## Tech stack

* **Python 3.6:** Programming language
* **Selenium:** Web automation framework
* **Chromium browser:** Web browser, run in headless mode
* **Flask:** Micro web server

## Requirements

* Python 3.6+
* Selenium
* Chromium browser
* Flask

## Installation

1. Install Python 3.6 or newer.
2. Install Selenium:

    ```
    pip install selenium
    ```

3. Install Chromium browser:

    ```
    sudo apt install chromium-browser
    ```

4. Install Flask:

    ```
    pip install Flask
    ```

5. Clone this repository:

    ```
    git clone https://github.com/gabrielkheisa/instagram-downloader.git
    ```

### With Dockerfile

1. Build the Dockerfile

    ```
    sudo docker build -t instagram-downloader .
    ```

2. Run the container

    ```
    sudo docker run -d -p 8080:8080 instagram-downloader
    ```

### With existing Docker Image

1. Pull the Docker image

    ```
    sudo docker pull ghcr.io/gabrielkheisa/instagram-downloader/gabrielkheisa/instagram-downloader:latest
    ```

2. Run the container

    ```
    sudo docker run -d -p 8080:8080 ghcr.io/gabrielkheisa/instagram-downloader/gabrielkheisa/instagram-downloader
    ```


## Usage

1. Start the Flask app, skip this part if you use Docker:

    ```
    python run.py
    ```

2. Open a web browser and navigate to http://localhost:8080/.
3. Add the query parameters of your Instagram Reels endpoint, for example for the original Instagram URL:
```
https://www.instagram.com/reel/Cz3dNmDMVC9/?igshid=MzRlODBiNWFlZA==
```
To be filled with:
```
http://localhost:8080/reel/Cz3dNmDMVC9/?igshid=MzRlODBiNWFlZA==
```
4. After you have something like https://scontent.cdninstagram.com/v/t66.30..., simply download the video
5. If the Instagram Reels video exists or no exception or error occurs, you will be redirected to the Instagram CDN endpoint link where you can download the video directly, else it will redirect to instagram.com

## Limitations

* It takes 3 to 5 seconds for the Xpath in the remote URL (instagram.com) to be loaded properly, so delay is **implicitly inserted** in the webdriver, making the request relatively longer for each invocation.
* It's possible that Instagram will change their Xpath website structure in the future, so you need to find the new Xpath location. Current Xpath and property:
```
/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/div[1]/div/article/div/div[1]/div/div/div/div/div/div/div/video
```
```
src
```
