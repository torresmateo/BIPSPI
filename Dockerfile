FROM continuumio/anaconda3:2023.07-1

RUN conda --version

# installing specific dependencies
WORKDIR /root

RUN apt-get update && apt-get install -y build-essential
# RUN apt-get install software-properties-common
# RUN apt-get update
# RUN add-apt-repository ppa:rock-core/qt4
# RUN apt-get update
# RUN apt-get install -y build-essential qt4
# RUN wget http://complex.zesoi.fer.hr/data/PSAIA-1.0-source.tar.gz



