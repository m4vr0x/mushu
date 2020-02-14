FROM mongo

ARG LOCALE="fr_FR ISO-8859-1"
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    vim \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    locales \
    && sed -i -e 's/# $LOCALE\(.*\)/$LOCALE\1/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=$LOCALE \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

RUN pip3 install pymongo pymediainfo

ENV LANG $LOCALE
ENV LC_ALL $LOCALE
