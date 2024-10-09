#Notes!!!: tag local docker image to djangotodo.azurecr.io/django-web

# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /code/

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run Django development server
CMD ["python", "playground/manage.py", "runserver", "0.0.0.0:8000"]

