from ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common

RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt update 
RUN apt install -y gdal-bin python-gdal python3-gdal

