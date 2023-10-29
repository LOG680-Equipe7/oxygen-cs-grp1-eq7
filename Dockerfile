# Use the official Python image as the base image
FROM python:3.8-alpine

# Set the working directory to /app
WORKDIR /app

# Force the resuling virtual environment to be created as /app/.venv.
ENV PIPENV_VENV_IN_PROJECT=1

# Other environment variables
ENV PYTHONUNBUFFERED=1

ENV HOST="https://hvac-simulator-a23-y2kpq.ondigitalocean.app"
ENV TOKEN="9vXWwTEL39"
ENV T_MAX="100"
ENV T_MIN="0"

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv
RUN pip install --upgrade pip
RUN pip install --upgrade pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/
RUN pip install psycopg2-binary

# Install dependencies
RUN pipenv install --system --deploy --ignore-pipfile

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python", "src/main.py"]
