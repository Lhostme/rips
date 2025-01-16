# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
# COPY requirements.txt .

# Install the dependencies
RUN pip install opencv-python-headless
RUN pip install flask
RUN pip install moviepy

# Copy the rest of your application code
COPY . .

EXPOSE 5000

# Run the application
CMD ["python", "your_script.py"]
