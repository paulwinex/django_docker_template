# -*- coding: utf-8 -*-
import re
import sys


import argparse
import sys
import os

from redis import Redis
from rq_scheduler.scheduler import Scheduler

from rq_scheduler.utils import setup_loghandlers


class MyScheduler(Scheduler):
    def enqueue_job(self, job):
        super(MyScheduler, self).enqueue_job(job)
        print('>>>>>>> Pushing {0} to {1}'.format(job.id, job.origin))


def main():
    parser = argparse.ArgumentParser(description='Runs RQ scheduler')
    parser.add_argument('-b', '--burst', action='store_true', default=False, help='Run in burst mode (quit after all work is done)')
    parser.add_argument('-H', '--host', default=os.environ.get('RQ_REDIS_HOST', 'localhost'), help="Redis host")
    parser.add_argument('-p', '--port', default=int(os.environ.get('RQ_REDIS_PORT', 6379)), type=int, help="Redis port number")
    parser.add_argument('-d', '--db', default=int(os.environ.get('RQ_REDIS_DB', 0)), type=int, help="Redis database")
    parser.add_argument('-P', '--password', default=os.environ.get('RQ_REDIS_PASSWORD'), help="Redis password")
    parser.add_argument('--verbose', '-v', action='store_true', default=False, help='Show more output')
    parser.add_argument('--url', '-u', default=os.environ.get('RQ_REDIS_URL')
        , help='URL describing Redis connection details. \
            Overrides other connection arguments if supplied.')
    parser.add_argument('-i', '--interval', default=60.0, type=float
        , help="How often the scheduler checks for new jobs to add to the \
            queue (in seconds, can be floating-point for more precision).")
    parser.add_argument('--path', default='.', help='Specify the import path.')
    parser.add_argument('--pid', help='A filename to use for the PID file.', metavar='FILE')

    args = parser.parse_args()

    if args.path:
        sys.path = args.path.split(':') + sys.path

    if args.pid:
        pid = str(os.getpid())
        filename = args.pid
        with open(filename, 'w') as f:
            f.write(pid)

    if args.url is not None:
        connection = Redis.from_url(args.url)
    else:
        connection = Redis(args.host, args.port, args.db, args.password)

    if args.verbose:
        level = 'DEBUG'
    else:
        # level = 'INFO'
        level = 'WARNING'
    setup_loghandlers(level)

    scheduler = MyScheduler(connection=connection, interval=args.interval)
    print('START SCHEDULER')
    try:
        scheduler.run(burst=args.burst)
    except Exception as e:
        print('ERROR', str(e))
        # input()
        return


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())