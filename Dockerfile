# Official Python image
FROM python:3.9-slim-buster

# Flask app default port
EXPOSE 5000

RUN apt-get update \
    && apt-get install -y mediainfo \
    wget \
    && wget https://mediaarea.net/repo/deb/repo-mediaarea_1.0-13_all.deb \
    && dpkg -i repo-mediaarea_1.0-13_all.deb

COPY app /app/
# Sets the working directory for following instructions
WORKDIR /app

RUN pip3 install -r requirements.txt

# Run web.py when the container launches
CMD python web.py
