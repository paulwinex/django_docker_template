#!/usr/bin/env bash
# https://github.com/ui/rq-scheduler
rqscheduler --host redis --port 6379 --db 0 -i 10
