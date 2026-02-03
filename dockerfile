# Use a lightweight Python version
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set up the app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--timeout", "120"]
