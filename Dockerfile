FROM python:slim-buster

ARG PIP_PACKAGES="pymongo"

RUN apt-get install -qqy \
      sudo \
      git \
      mongo \
      python3-pip \
      python3-dev \
      python3-setuptools \
      python3-wheel && \
    rm -rf /var/lib/apt/lists/* && \
    rm -Rf /usr/share/doc && rm -Rf /usr/share/man && \
    apt-get clean

RUN pip3 install $PIP_PACKAGES
