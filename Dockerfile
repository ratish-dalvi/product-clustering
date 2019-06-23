FROM continuumio/miniconda:4.3.11

WORKDIR /usr/src/app

COPY environment.yml .

RUN conda env create -f environment.yml

ENV PATH /opt/conda/envs/product_clustering/bin:$PATH
ENV CONDA_DEFAULT_ENV product_clustering
ENV CONDA_PREFIX /opt/conda/envs/product_clustering

COPY . .

# RUN pip install .

# ENTRYPOINT ["product_clustering"]
