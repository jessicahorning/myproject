# Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "app.py"]