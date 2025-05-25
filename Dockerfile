# Use the official Python image from the Docker Hub
FROM python:3.10-alpine as base

# Set the working directory
WORKDIR /app

COPY pyproject.toml .

RUN pip install uv
RUN uv sync --frozen --no-install-project --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Copy the project files
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
