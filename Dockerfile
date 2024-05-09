# Build Stage
FROM python:3.9 AS builder

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Run tests
RUN python -m unittest discover -s tests -p "test_main.py" \
    && echo "Tests passed. Building Docker image." \
    || (echo "Tests failed. Cannot proceed with image build." && exit 1)

# Production Stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only the application code from the build stage
COPY --from=builder /app .
RUN pip install --no-cache-dir -r requirements.txt


# Command to run the application
CMD ["python", "main.py"]
