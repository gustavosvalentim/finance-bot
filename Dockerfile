# Use the official Python image from the Docker Hub
FROM python:3.9-slim as base

COPY requirements.txt .
RUN pip install -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
