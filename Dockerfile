FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      clang \
      golang-go \
      openjdk-17-jdk \
      python3 \
      python3-pip \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN mkdir -p /app/results

ENTRYPOINT ["python3", "run_all.py"]