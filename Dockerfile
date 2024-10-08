# Use the official Python base image
FROM python:3.11.7

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]