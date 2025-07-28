# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements first and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 5000

# Start the Flask app using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
