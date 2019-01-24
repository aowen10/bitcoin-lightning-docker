#!/usr/bin/env bash

# exit from script if error was raised.
set -e

# error function is used within a bash function in order to send the error
# message directly to the stderr output and exit.
error() {
    echo "$1" > /dev/stderr
    exit 0
}

# return is used within bash function in order to return the value.
return() {
    echo "$1"
}

# set_default function gives the ability to move the setting of default
# env variable from docker file to the script thereby giving the ability to the
# user override it during container start.
set_default() {
    # docker initialized env variables with blank string and we can't just
    # use -z flag as usually.
    BLANK_STRING='""'

    VARIABLE="$1"
    DEFAULT="$2"

    if [[ -z "$VARIABLE" || "$VARIABLE" == "$BLANK_STRING" ]]; then

        if [ -z "$DEFAULT" ]; then
            error "You should specify default variable"
        else
            VARIABLE="$DEFAULT"
        fi
    fi

   return "$VARIABLE"
}


# Set default variables if needed.
RPCHOST=$(set_default "$RPCHOST" "127.0.0.1")
ZMQ_PUB_RAW_BLOCK=$(set_default "$ZMQ_PUB_RAW_BLOCK" "tcp://127.0.0.1:28333")
ZMQ_PUB_RAW_TX=$(set_default "$ZMQ_PUB_RAW_TX" "tcp://127.0.0.1:28333")
RPCUSER=$(set_default "$RPCUSER" "devuser")
RPCPASS=$(set_default "$RPCPASS" "devpass")
RPCAUTH=$(set_default "$RPCAUTH" "user:d4a9dfedc252bb9a40b62a541822f26$45ac142a1c62a5856671531684f95a525556156793f1a696d25ed64a4609233b")
DEBUG=$(set_default "$DEBUG" "debug")
NETWORK=$(set_default "$NETWORK" "testnet")
CHAIN=$(set_default "$CHAIN" "bitcoin")
BITCOIN_NODE=$(set_default "$BITCOIN_NODE" "bitcoind")
BACKEND="bitcoind"

RPC_LISTEN=$(set_default "$RPC_LISTEN" ":10009")
REST_LISTEN=$(set_default "$REST_LISTEN" ":8080")
LISTEN=$(set_default "$LISTEN" ":9735")
LNDCONFLOC=$(set_default "$LNDCONFLOC" "/root/.lnd/lnd.conf")
#Where the file will be copied to by the DockerFile
LNDCONFCOPYLOC=$(set_default "$LNDCONFCOPYLOC" "/lnd.conf")


if [ -e $LNDCONFCOPYLOC ]; then
        mv $LNDCONFCOPYLOC $LNDCONFLOC
fi

echo "running lnd"
exec lnd \
    --configfile=/root/.lnd/lnd.conf
    "$@"