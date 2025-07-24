FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (optional but useful)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean    

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . /app/

# Expose port
EXPOSE 5000

# Run the Flask app (if using `wsgi.py`)
CMD ["flask", "run", "--host=0.0.0.0"]
