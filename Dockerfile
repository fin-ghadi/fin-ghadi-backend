# Use the official Python image from Docker Hub
FROM python:3.12.3

# Set the working directory inside the container
WORKDIR /app.main

# Copy the requirements file to the working directory
COPY requirements.txt .

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]
