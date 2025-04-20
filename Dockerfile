FROM python:3.9-slim

# Install wkhtmltopdf and dependencies
RUN apt-get update && apt-get install -y wkhtmltopdf libssl-dev ca-certificates libfontconfig1 fonts-roboto && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Run Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]