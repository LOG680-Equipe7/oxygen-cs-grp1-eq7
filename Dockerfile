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

# Copy only specific files at the root
COPY docker-compose.yml /app/
COPY Dockerfile /app/
COPY requirements.txt /app/
COPY src/ /app/src/

# Install pipenv
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pip install -r requirements.txt
RUN pipenv install --system --deploy --ignore-pipfile

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python", "src/main.py"]
