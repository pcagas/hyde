FROM continuumio/anaconda:latest

WORKDIR /home/hyde

COPY environment.yml ./
COPY hyde-api-server ./
COPY hyde/ ./hyde

RUN conda env create -f environment.yml

RUN echo "source activate hyde" > ~/.bashrc
ENV PATH /opt/conda/envs/hyde/bin:$PATH

EXPOSE 3000

ENTRYPOINT python hyde-api-server