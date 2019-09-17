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
         tree

RUN curl -o miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x miniconda.sh && \
     ./miniconda.sh -b -p /opt/conda && rm miniconda.sh && \
     /opt/conda/bin/conda install -y numpy pyyaml scipy pandas ipython mkl mkl-include && \
     /opt/conda/bin/conda install pytorch=1.2.0 torchvision cudatoolkit=10.0 -c pytorch && \
     /opt/conda/bin/conda clean -ya

ENV PATH /opt/conda/bin:$PATH

RUN pip install kiwisolver matplotlib numpy tqdm


