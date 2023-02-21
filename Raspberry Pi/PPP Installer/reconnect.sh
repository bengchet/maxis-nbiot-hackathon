#!/bin/sh

while true; do

        ifconfig ppp0

        if [ $? -eq 0 ]; then
                echo "Connection up, reconnect not required..."
        else
                echo "Connection down, reconnecting..."
                sudo ifconfig wwan0 down
                sudo pon
        fi

        sleep 10
done