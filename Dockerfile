# Use an official Python runtime as the base image
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile* /app/

# Install the dependencies using Pipenv
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

# Copy the rest of the application code to the container
COPY . /app/

EXPOSE 8000