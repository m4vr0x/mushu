FROM python:slim-buster

ARG PIP_PACKAGES="pymongo"

RUN apt-get update && apt-get install -qqy \
      sudo \
      wget && \
      wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add - && \
      echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list && \
      apt-get update && apt-get install -qqy \
      mongodb-org && \
      # python3-pip \
      # python3-dev \
      # python3-setuptools \
      # python3-wheel && \
    rm -rf /var/lib/apt/lists/* && \
    rm -Rf /usr/share/doc && rm -Rf /usr/share/man && \
    apt-get clean

RUN pip3 install $PIP_PACKAGES
