FROM ubuntu:latest
LABEL authors="sightless"

ENTRYPOINT ["top", "-b"]