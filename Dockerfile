FROM mongo

RUN add-apt-repository universe \
    apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    vim \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

RUN pip3 install pymongo pymediainfo

RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
