# Use the official Selenium standalone Chrome image as base
FROM selenium/standalone-chrome:112.0.5615.165-chromedriver-112.0.5615.49

ENV DEBIAN_FRONTEND=noninteractive

# Update package lists
RUN sudo apt-get update

# Install Python 3.6 and pip
RUN sudo apt-get install -y python3

RUN sudo apt-get install -y python3-pip

# Install Selenium and any other Python dependencies you may need
RUN sudo pip install selenium==3.141.0
RUN sudo pip install --upgrade urllib3==1.26.16
RUN sudo pip install Flask

# Set the working directory
WORKDIR /usr/src/app

# Copy your Python scripts into the container
COPY . .

EXPOSE 8080

# Example command to run your Python script
CMD ["python3", "run.py"]
