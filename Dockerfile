# Use an official Python runtime as the base image
FROM python:slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script to the working directory
COPY main.py .
COPY azure_document_intelligence.py .

# Install any dependencies if required
# For example, if you have a requirements.txt file:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Run the Python script when the container starts
CMD ["python", "main.py"]