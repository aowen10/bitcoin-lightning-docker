ARG lndconf

FROM golang:alpine as builder

# Force Go to use the cgo based DNS resolver. This is required to ensure DNS
# queries required to connect to linked containers succeed.
ENV GODEBUG netdns=cgo

# Comments below are the way that PierreRochard repo downloaded and installed lnd
# Install dependencies and install/build lnd.

RUN apk add --no-cache --update alpine-sdk \
    git \
    make \
    gcc \
&&  git clone https://github.com/lightningnetwork/lnd /go/src/github.com/lightningnetwork/lnd \
&&  cd /go/src/github.com/lightningnetwork/lnd \
&&  make \
&&  make install

# WORKDIR $GOPATH/src/github.com/LN-Zap/zapconnect
# RUN git clone https://github.com/LN-Zap/zapconnect . \
#   && git reset --hard 7c3c72adb6fbfcf343570839124013bbc4649f08 \
#   && make \
#   && make install
  # Don't need this line because they're redone later
  # && cp /go/bin/zapconnect /bin/


# Start a new, final image to reduce size.
FROM alpine as final

# Copy the binaries and entrypoint from the builder image.
COPY --from=builder /go/bin/lncli /bin/
COPY --from=builder /go/bin/lnd /bin/
# COPY --from=builder /go/bin/zapconnect /bin/

# Add bash. (and curl)
RUN apk add --no-cache \
    bash

# Copy the entrypoint script.
COPY "start-lnd.sh" .
#Potentially COPY a lnd.conf file, and remove it from the start-lnd.sh?
#RUN mkdir /root/.lnd 
#COPY "lnd-mainnet.conf" .
#COPY "lnd-testnet.conf" .
RUN echo ${lndconf}
#COPY $lndconf .
RUN chmod +x start-lnd.sh

