FROM python:3.7

# Install stuff
RUN apt-get update && apt-get -y install apt-file && apt-file update && \
    apt-get -y install vim git gcc gfortran

RUN mkdir /app && mkdir /app/pypride && mkdir /data

# copy over the code
ADD setup.py /app
ADD pypride/ /app/pypride/

WORKDIR /app

# install pypride
RUN pip install numpy && python setup.py install --record files.txt

CMD /bin/bash
