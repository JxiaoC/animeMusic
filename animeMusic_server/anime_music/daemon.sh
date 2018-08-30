#!/bin/bash

usage="Usage: $0 [start | stop]"

PORT_RANGE="12040 12043"
service="anime-music-server"
LOG_DIR="/tmp/jijidown/$service"
pid="$LOG_DIR/service.pid"
log="$LOG_DIR/service.log"


ROOTDIR=$(dirname $0)
MAIN=$ROOTDIR/main.py


if [ ! -d $LOG_DIR ]; then
    mkdir -p "$LOG_DIR"
fi

case $1 in
    (start)

        for i in `seq $PORT_RANGE`
        do
            _pid=$pid.$i
            if [ -f $_pid ]; then
                if kill -0 `cat $_pid` > /dev/null 2>&1; then
                    echo $service running as process `cat $_pid`. Stop it first.
                    exit 1
                fi
            fi

            echo [port: $i] starting $service ...

            nohup python $MAIN --port=$i >"$log.$i" 2>&1 < /dev/null &
            echo $! > "$_pid"
            sleep 0.5; head "$log.$i"
        done
        ;;

    (stop)

        for i in `seq $PORT_RANGE`
        do
            _pid=$pid.$i
            if [ -f $_pid ]; then
                if kill -0 `cat $_pid` > /dev/null 2>&1; then
                    echo [port: $i] stopping $service `cat $_pid`...
                    kill `cat $_pid`
                else
                    echo no $service to stop
                fi
            else
                echo no $service to stop
            fi
        done
        ;;

    (test)

        python $MAIN --port=9000
        ;;

    (*)
        echo $usage
        exit 1
        ;;

esac
