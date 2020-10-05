# Official Python image
FROM python:3.6

# Flask app default port
EXPOSE 5000

COPY app /app/
# Sets the working directory for following instructions
WORKDIR /app

RUN wget https://mediaarea.net/repo/deb/repo-mediaarea_1.0-13_all.deb \
    && dpkg -i repo-mediaarea_1.0-13_all.deb \
    && apt-get update \
    && apt-get install -y mediainfo
# Install pip packages specified in requirements.txt
RUN pip install -r requirements.txt
# Run web.py when the container launches
CMD python web.py
