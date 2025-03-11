# Base image
FROM python:3.11.1-slim

# Set working directory
WORKDIR /app

# Install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# Copy PDM project files
COPY pyproject.toml pdm.lock README.md ./

# Copy application code
COPY src/ ./src/

# Install dependencies using PDM
RUN pdm install --production

# Set environment variables
RUN export PYTHONPATH=${PYTHONPATH}:$(pdm info --python-path)
ENV PORT=8080

# Expose port
EXPOSE ${PORT}

# Command to run the application
CMD ["pdm", "run", "start"]