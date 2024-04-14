# Use an official Python runtime as a parent image
FROM python:3.12.2-bookworm
# Set environment variables
ENV WORKER_COUNT 4

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /app
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code into the container
COPY ./app /code/app

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the FastAPI app using uvicorn when the container launches
CMD gunicorn -w ${WORKER_COUNT} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app
