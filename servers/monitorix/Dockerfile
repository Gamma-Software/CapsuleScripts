# syntax=docker/dockerfile:1
FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install monitorix -y
ENTRYPOINT service monitorix start && /bin/bash
