FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

WORKDIR /workspace
RUN chmod -R a+w /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
         cmake \
         curl \
         build-essential \
         less \
         screen \
         vim \
         git \
         htop \
         wget \
         jq \
         tree \
         libboost-all-dev

RUN curl -o miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x miniconda.sh && \
     ./miniconda.sh -b -p /opt/conda && rm miniconda.sh && \
     /opt/conda/bin/conda install -y numpy pyyaml scipy pandas ipython mkl mkl-include && \
     /opt/conda/bin/conda install pytorch=1.2.0 torchvision cudatoolkit=10.0 -c pytorch && \
     /opt/conda/bin/conda clean -ya
ENV PATH /opt/conda/bin:$PATH

RUN cd / && git clone https://github.com/dds-bridge/dds && cd /dds && git checkout 9c554cc
RUN cd /dds/src && cp Makefiles/Makefile_linux_shared ./Makefile && make

RUN cd / && git clone https://github.com/Afwas/python-dds && cd /python-dds && git checkout 653dbd5
RUN cp /dds/src/libdds.so /usr/lib/libdds.so

RUN pip install kiwisolver matplotlib numpy tqdm


