FROM golang:1.10-alpine as builder

# Force Go to use the cgo based DNS resolver. This is required to ensure DNS
# queries required to connect to linked containers succeed.
ENV GODEBUG netdns=cgo

# Install dependencies and install/build lnd.
RUN apk add --no-cache git make bash
RUN go get -u github.com/golang/dep/cmd/dep
RUN go get -d github.com/lightningnetwork/lnd
RUN  cd /go/src/github.com/lightningnetwork/lnd &&  make &&  make install

WORKDIR $GOPATH/src/github.com/LN-Zap/zapconnect
RUN git clone https://github.com/LN-Zap/zapconnect . \
  && git reset --hard 7c3c72adb6fbfcf343570839124013bbc4649f08 \
  && make \
  && make install \
  && cp /go/bin/zapconnect /bin/

# Start a new, final image to reduce size.
FROM alpine as final

# Copy the binaries and entrypoint from the builder image.
COPY --from=builder /go/bin/lncli /bin/
COPY --from=builder /go/bin/lnd /bin/
COPY --from=builder /go/bin/zapconnect /bin/

# Add bash.
RUN apk add --no-cache \
    bash

# Copy the entrypoint script.
COPY "start-lnd.sh" .
RUN chmod +x start-lnd.sh
