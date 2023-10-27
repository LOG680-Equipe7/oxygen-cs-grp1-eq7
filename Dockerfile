# Use the official Python image as the base image
FROM python:3.11-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Force the resuling virtual environment to be created as /app/.venv.
ENV PIPENV_VENV_IN_PROJECT=1

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --system --deploy --ignore-pipfile
RUN pipenv install signalrcore

# Make port 8000 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["pipenv", "run", "start"]
