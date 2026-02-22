# Use the official Python slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies needed for the webhook receiver and tests
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv requests numpy pandas

# Expose port (FastAPI usually runs on 8000)
EXPOSE 8000

# Command to run the webhook receiver
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
