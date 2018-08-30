#!/usr/bin/env bash

ROOTDIR=$(pwd)/$(dirname $0)

$ROOTDIR/daemon.sh stop && sleep 1 && $ROOTDIR/daemon.sh start
