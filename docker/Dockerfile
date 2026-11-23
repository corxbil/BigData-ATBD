FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    python3 \
    python3-pip \
    openssh-client \
    openssh-server \
    curl \
    wget \
    procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

CMD ["bash"]
