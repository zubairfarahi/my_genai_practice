# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY src ./src

# Expose necessary ports
EXPOSE 7860

# Command to run Chainlit app
CMD ["chainlit", "run", "src/main.py", "--host", "0.0.0.0", "--port", "7860"]
