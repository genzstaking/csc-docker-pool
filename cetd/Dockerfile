FROM golang:1.18-buster as build
WORKDIR /build
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
       build-essential \
       git \
       make 

# Install bech32
ARG VERSION
RUN echo "Building tags/v$VERSION..." \
    && git clone https://github.com/coinex-smart-chain/csc.git \
    && cd csc \
    && git fetch --all --recurse-submodules --tags \
    && git tag \
    && git checkout tags/v$VERSION \
    && make cetd


# Run
FROM debian:buster
RUN apt-get update \
    && apt-get install --no-install-recommends  -y \
    ca-certificates \
    && update-ca-certificates --fresh \
    && apt-get clean
COPY --from=build /build/csc/build/bin /bin

ENTRYPOINT ["cetd"]