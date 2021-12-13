# It is used to run PotreeConverter in docker
# Function: convert point clout to potree format and generate html for potree view
# Command: sudo docker build -t potreetransform .
# Run: see run.sh
# Reference: https://github.com/potree/PotreeConverter/issues/180


FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y \
    gcc \
    g++ \
    gdb \
    cmake
    # && apt-get clean

# python3  
RUN apt-get update && apt-get install -y software-properties-common
RUN sh -c '/bin/echo -e "\n" | add-apt-repository ppa:deadsnakes/ppa' \
    && apt-get install -y python3.8 python3-pip
    # && ln -s /usr/bin/python3.8 /usr/bin/python3

RUN  apt update && apt install -y git

RUN git clone https://github.com/m-schuetz/LAStools.git \
    && cd LAStools/LASzip \
    && mkdir build && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Release .. \
    && make


RUN apt-get install libtbb2 libtbb-dev \
    && git clone https://github.com/potree/PotreeConverter.git \
    && cd PotreeConverter \
    && mkdir build && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Release -DLASZIP_INCLUDE_DIRS=/LAStools/LASzip/build/src/liblaszip.so .. \
    && make 

# RUN apt-get install libtbb-dev  

RUN mkdir -p /usr/src/app \
    && cp -rf /PotreeConverter/build/* /usr/src/app/

WORKDIR /usr/src/app
COPY . /usr/src/app
ENV HOME=/usr/src/app


