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
EXPOSE 8000

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Run the application
CMD ["pipenv", "run", "python", "app.py"]

