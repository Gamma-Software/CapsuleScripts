# Use Python image as base
FROM python:3

# Set working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY locate.py /app/locate.py

# Install necessary libraries
RUN pip install folium paho-mqtt

# Expose port for Flask server
EXPOSE 5000

# Install Flask and gunicorn
RUN pip install flask gunicorn

# Define the command to run your script
CMD gunicorn -b 0.0.0.0:5000 -w 1 locate:app
