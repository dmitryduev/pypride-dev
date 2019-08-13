FROM python:3.7

# Install stuff
RUN apt-get update && apt-get -y install apt-file && apt-file update && \
    apt-get -y install vim git gcc gfortran



CMD /bin/bash
