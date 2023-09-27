FROM ubuntu:22.04

# taken from https://stackoverflow.com/a/58269633
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
RUN conda --version

# installing specific dependencies
RUN wget http://bioinfo.zesoi.fer.hr/data/PSAIA-1.0-linux-installer.bin \
    && chmod 774 PSAIA-1.0-linux-installer.bin \
    && ./PSAIA-1.0-linux.installer.bin



