# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port for Railway to bind to
EXPOSE 5000

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
