FROM ghcr.io/contextmachine/mmcore:latest

LABEL authors="sth-v"
COPY . .
RUN python3 setup.py build_ext --inplace
