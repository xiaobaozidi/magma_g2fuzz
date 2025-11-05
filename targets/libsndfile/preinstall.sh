#!/bin/bash
apt-get update && \
    apt-get install -y git make autoconf autogen automake build-essential \
  libtool pkg-config python3 python-is-python3
