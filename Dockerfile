# # Use an official Python runtime as the base image
# FROM python:3.10

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the Pipfile and Pipfile.lock to the container
# COPY Pipfile* /app/

# # Install dependencies using Pipenv
# RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# # Copy the rest of the application code to the container
# COPY . /app/

# # Collect static files (if applicable)
# RUN python manage.py collectstatic --noinput

# # Migrate the database (if applicable)
# RUN python manage.py migrate

# # Expose the port on which the Django application will run
# EXPOSE 8000

# # Command to run the application
# CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

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