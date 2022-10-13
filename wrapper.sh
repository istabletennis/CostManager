#!/bin/bash
python3 app.py &&
sleep 10 &
python3 service.py
wait -n
exit $?

