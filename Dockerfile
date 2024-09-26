# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

# Copy the application code into the container
COPY src/ app

# Expose the port that the app will run on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]

