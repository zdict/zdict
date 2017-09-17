FROM ubuntu:16.04

# Set the locale
RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install Python3 & pip3
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# Install zdict
WORKDIR /srv/work/
ADD . /srv/work/
RUN pip3 install -e .

ENTRYPOINT ["zdict"]
