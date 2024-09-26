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

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Create a directory for the database
RUN mkdir /data

# Set permissions for the database directory
RUN chmod 777 /data

# Set environment variable for database path
ENV DATABASE_URL=sqlite:////data/receipts.db


# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]

