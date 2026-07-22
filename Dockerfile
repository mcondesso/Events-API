# Use base image
FROM python:3.11-slim

# set a working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . .

# Run app
CMD ["python", "app.py"]