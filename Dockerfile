# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
# COPY requirements.txt .

# Install the dependencies
RUN pip install opencv-python-headless

# Copy the rest of your application code
COPY . .

# Run the application
CMD ["python", "your_script.py"]
