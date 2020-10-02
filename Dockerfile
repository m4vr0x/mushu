# Official Python image
FROM python:3.6

# Flask app default port
EXPOSE 5000

COPY app /app/

# Sets the working directory for following instructions
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run web.py when the container launches
CMD python web.py
