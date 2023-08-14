FROM ghcr.io/contextmachine/mmcore:latest

LABEL authors="andrewastakhov"
WORKDIR mmcore
COPY . .
RUN python3 setup.py build_ext --inplace
ENTRYPOINT ["python3"]