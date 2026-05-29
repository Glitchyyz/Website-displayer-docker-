FROM python:3.11-slim

WORKDIR /app

# Copy the server script
COPY server.py .

# Create the html directory
RUN mkdir -p html



# Expose port 8000
EXPOSE 8000

# Run the server
CMD ["python3", "server.py"]
