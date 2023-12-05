FROM python:3.9-slim

# Set the working directory to /app/store-monitoring/app
WORKDIR /app

# Copy the current directory contents into the container at /app/store-monitoring/app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]